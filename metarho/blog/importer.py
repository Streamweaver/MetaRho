# file importer.py
#
# Copyright 2010 Scott Turnbull
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, softwaretributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import sys
import re
from datetime import datetime
from urlparse import urlparse
from xml.etree import ElementTree

from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions  import ObjectDoesNotExist

from tagging.models import Tag

from metarho.blog.models import Post
from metarho.blog.models import PostMeta
from metarho.sitemeta.models import SiteInformation

class WordPressExportParser:
    '''
    Class for parsing Wordpress XML Export Files and Importing into app.

    Some code pulled from
    http://www.beardygeek.com/2009/01/from-wordpress-to-django-part-two/
    '''

    blog = []
    _author = None
    _pub = None

    def __init__(self, file, username):
        try:
            self.tree = ElementTree.parse(file)
            self.chan = self.tree.find('channel')
            self.wp_ns = '{http://wordpress.org/export/1.1/}'
            self.content_ns = '{http://purl.org/rss/1.0/modules/content/}'
            self.dc_ns = '{http://purl.org/dc/elements/1.1/}'
            self.excerpt_ns = '{http://wordpress.org/export/1.0/excerpt/}'
            try: # Need an owner to assosite the site information and posts to.
                self.owner = User.objects.get(username=username)
            except User.DoesNotExist:
                raise ObjectDoesNotExist('No usre exists matching %s' % username)
        except IOError:
            sys.stderr.write("File Not Found!: %s" % file)

    def parse(self):
        '''Initiates all import operations on a file.'''
        #self.import_site_information()
        self.import_posts()

    def set_author(self, user):
        '''Sets the default author for all posts imported.'''
        self._author = user

    def get_author(self):
        '''Returns the author user or site owner if none.'''
        if not self._author:
            return self.owner
        return self._author

    def import_site_information(self):
        '''
        Imports Site Information from the file into a new SiteInformation
        object so it can be set as the default later if appropriate.

        '''
        # Create the Site object
        url = urlparse(self.chan.find(self.wp_ns + 'base_blog_url').text)
        name = self.chan.find('title').text
        site = Site(domain=url.netloc, name=name)
        site.save()

        # Create SiteInformation object.
        info = SiteInformation()
        info.title = name
        info.default = False # Don't override any site settings.
        info.description = self.chan.find('description').text
        info.site = site
        info.owner = self.owner
        info.save()

    def import_posts(self):
        '''Parses the Export File.'''
        items = self.chan.findall('item')
        for item in items:
            self._import_post(item)

    def _import_post(self, item):
        '''Creates a new Entry object from a post and saves it.'''
        wp_ns = self.wp_ns
        content_ns = self.content_ns

        if item.find(wp_ns + 'post_type').text == 'post':
            # These methods are only for scrubbing my crappy content.
            # @TODO remove after I run on my blog.
            item_title = item.find('title').text
            item_content = item.find(content_ns + 'encoded').text
            if item_title and re.search('From Twitter ', item_title):
                print "Skipping tittinisis post %s" % item_title
                return True
            # @TODO remove after I run on my blog.
            if item_content and re.search('LoudTwitter', item_content):
                print "Skipping loudtwitter post %s" % item.find('title').text
                return True
            post = Post()
            post.author = self.get_author()
            post.title = item_title
            if post.title and len(post.title) > 75:
                post.title = post.title[:75]
            if not post.title:
                post.title = 'ab origine' # Latin for 'from the source'
            post.content = item_content
            if post.content:
                post.content = post.content.replace("\n", "<br />")
            excerpt = item.find(self.excerpt_ns + 'encoded')
            if excerpt:
                post.teaser = excerpt.text
            # Parse wp:post_date in format 2002-02-27 13:39:00
            postdate = datetime.strptime(item.find(wp_ns + 'post_date').text, "%Y-%m-%d %H:%M:%S")
            post.pub_date = postdate
            status = item.find(wp_ns + 'status').text
            if status == 'publish':
                post.status = 'P'
            else:
                post.status = 'U'
            #try:
            post.save()

            # modify date_created after save because autonow is on.
            post.date_created = postdate
            post.save()
            # Enrich the rest of the post.
            self._post_meta(post, item)
            self._catalog_post(post, item)

            #except:
#                sys.stderr.write("Error importing %s" % post.title)
#                pass

    def _post_meta(self, post, item):
        '''Create Post Meta items.'''
        wi = PostMeta(post=post, key='wp_post_id',
                         value=item.find(self.wp_ns + 'post_id').text)
        wi.save()
        wbt = PostMeta(post=post, key='wp_blog_title',
                                 value=self.chan.find('title').text)
        wbt.save()
        wl = PostMeta(post=post, key='wp_blog_link',
                      value=self.chan.find('link').text)
        wl.save()
        wa = PostMeta(post=post, key='wp_author',
                      value=item.find(self.dc_ns + 'creator').text)
        wa.save()
        # Construct the PostMeta information.
        post_meta = item.findall(self.wp_ns + 'postmeta')
        for meta in post_meta:
            try:
                pm = PostMeta()
                pm.post = post
                pm.key = meta.find(self.wp_ns + 'meta_key').text[:30]
                pm.value = meta.find(self.wp_ns + 'meta_value').text[:255]
                pm.save()
            except: # @TODO change this to validation exception when 1.2 released.
                sys.stderr.write("Unable to save %s %s for post %s. Skipping." % (pm.key, pm.value, post.title))
                pass

    def _catalog_post_old(self, post, item):
        '''Build tags and topics for post.'''
        post_cats = item.findall('category')
        for pc in post_cats:
            #check for attributes
            if pc.get('nicename'):
                if pc.attrib['domain'] == 'category':
                    t = Topic.objects.get(slug=pc.attrib['nicename'])
                    tc = TopicCatalog(content_object=post, topic=t)
                    tc.save()
                elif pc.attrib['domain'] == 'tag':
                    t = Tag.objects.get(slug=pc.attrib['nicename'])
                    tc = TaggedItem(content_object=post, tag=t)
                    tc.save()

    def _catalog_post(self, post, item):
        """Adds catagory and tags to post tags.
        
            :param post: django post model
            :param item: parse wp item from xml
            """
        post_cats = item.findall('category')
        tags = [tag.text for tag in post_cats]
        post.tags = ', '.join(tags)
        post.save()


