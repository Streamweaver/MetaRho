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

import pyblog
import re

from django.contrib.auth.models import User

from metarho.blog.models import Post

import pprint

site = 'http://localhost/fwtd/xmlrpc.php'
user = 'admin'
passwd = 'p33kab00'
author = User.objects.get(pk=1)

class WordpressImporter:

    error_ids = []
    success_ids = []

    def __init__(self, url, user, pw, maxid, author):
        """Initializes a new wp importer """
        self.blog = pyblog.WordPress(url, user, pw)
        self.id_range = range(1, maxid)
        self.author = author

    def import_all(self):
        """Iterates overall posts in self.id_range and imports them."""
        for id in self.id_range:
            try:
                post = self.blog.get_post(id)
                self.import_post(post)
                self.success_ids.append(id)
            except pyblog.BlogError:
                self.error_ids.append(id)
        print "DONE! Imported %s and skipped %s" (len(self.success_ids), len(self.error_ids))

    def import_post(self, wp_post):
        # 'From Twitter 'in title
        # 'LoudTwitter'
        if re.search('From Twitter ', wp_post['title']):
            return True
        if re.search('LoudTwitter', wp_post['description']):
            return True
        post = Post()
        post.title = "No Title Given"
        if wp_post['title']:
            post.title =  wp_post['title']
        post.content = wp_post['description']
        post.slug = wp_post['wp_slug']
        post.pub_date = wp_post['dateCreated']
        post.author = self.author
        post.status = 'U'
        if wp_post['post_status'] == 'publish':
            post.status = 'P'
        post.save() # Set date created/modified so I can change them.
        post.date_created = wp_post['dateCreated']
        post.save()

#    {   'categories': ['Uncategorized'],
#        'custom_fields': [   {   'id': '6821', 'key': 'lj_itemid', 'value': '3055'},
#                             {   'id': '6822',
#                                 'key': 'lj_permalink',
#                                 'value': 'http://streamweaver.livejournal.com/782213.html'}],
#        'dateCreated': <DateTime '20110512T02:33:00' at b71aa22c>,
#        'date_created_gmt': <DateTime '20110512T02:33:00' at b71aa90c>,
#        'description': '<div>\n<div class="loudtwitter"><ul><li><a href="http://twitter.com/Streamweaver/statuses/68430855705604096">17:42:42</a>: Corruption Twin Powers Activate!  Form of a Comcast Lobbyist!  <a href="http://bit.ly/kYG3Qb">http://bit.ly/kYG3Qb</a> Oh yea, this is gonna be awesome. :(\n</li></ul></div>\n</div><p>Tweets copied by <a href="http://twittinesis.com">twittinesis.com</a></p>',
#        'link': 'http://localhost/fwtd/?p=3033',
#        'mt_allow_comments': 1,
#        'mt_allow_pings': 1,
#        'mt_excerpt': '',
#        'mt_keywords': '',
#        'mt_text_more': '',
#        'permaLink': 'http://localhost/fwtd/?p=3033',
#        'post_status': 'publish',
#        'postid': '3033',
#        'title': 'From Twitter 05-11-2011',
#        'userid': '1',
#        'wp_author_display_name': 'admin',
#        'wp_author_id': '1',
#        'wp_password': '',
#        'wp_post_format': 'standard',
#        'wp_slug': 'from-twitter-05-11-2011'}

importer = WordpressImporter(site, user, passwd, 30, author)
importer.import_all()

# Code below based on old xml file parser for wordpress.

#import sys
#from datetime import datetime
#from urlparse import urlparse
#from xml.etree import ElementTree
#
#from django.contrib.auth.models import User
#from django.contrib.sites.models import Site
#from django.core.exceptions  import ObjectDoesNotExist
#
#from metarho.blog.models import Post
#from metarho.blog.models import PostMeta
#from metarho.sitemeta.models import SiteInformation


# @TODO Rework this class when I have tagging and topics back in.
#class WordPressExportParser:
#    '''
#    Class for parsing Wordpress XML Export Files and Importing into app.
#
#    Some code pulled from
#    http://www.beardygeek.com/2009/01/from-wordpress-to-django-part-two/
#    '''
#
#    blog = []
#    _author = None
#    _pub = None
#
#    def __init__(self, file, username):
#        try:
#            self.tree = ElementTree.parse(file)
#            self.chan = self.tree.find('channel')
#            self.wp_ns = '{http://wordpress.org/export/1.0/}'
#            self.content_ns = '{http://purl.org/rss/1.0/modules/content/}'
#            self.dc_ns = '{http://purl.org/dc/elements/1.1/}'
#            self.excerpt_ns = '{http://wordpress.org/export/1.0/excerpt/}'
#            try: # Need an owner to assosite the site information and posts to.
#                self.owner = User.objects.get(username=username)
#            except User.DoesNotExist:
#                raise ObjectDoesNotExist('No usre exists matching %s' % username)
#        except IOError:
#            sys.stderr.write("File Not Found!: %s" % file)
#
#    def parse(self):
#        '''Initiates all import operations on a file.'''
#        self.import_site_information()
#        self.import_tags()
#        self.import_catagories()
#        self.import_posts()
#
#    def set_author(self, user):
#        '''Sets the default author for all posts imported.'''
#        self._author = user
#
#    def get_author(self):
#        '''Returns the author user or site owner if none.'''
#        if not self._author:
#            return self.owner
#        return self._author
#
#    def import_site_information(self):
#        '''
#        Imports Site Information from the file into a new SiteInformation
#        object so it can be set as the default later if appropriate.
#
#        '''
#        # Create the Site object
#        url = urlparse(self.chan.find(self.wp_ns + 'base_blog_url').text)
#        name = self.chan.find('title').text
#        site = Site(domain=url.netloc, name=name)
#        site.save()
#
#        # Create SiteInformation object.
#        info = SiteInformation()
#        info.title = name
#        info.default = False # Don't override any site settings.
#        info.description = self.chan.find('description').text
#        info.site = site
#        info.owner = self.owner
#        info.save()
#
#    def import_tags(self):
#        '''Import Tags.'''
#        tags = self.chan.findall(self.wp_ns + 'tag')
#        for tag in tags:
#            t = Tag()
#            t.text=tag.find(self.wp_ns + 'tag_name').text
#            t.slug=tag.find(self.wp_ns + 'tag_slug').text
#            t.save()
#
#    def import_catagories(self):
#        '''Parses and imports the catagories from a blog posts.'''
#        topics = self.chan.findall(self.wp_ns + 'category')
#        for topic in topics:
#            t = Topic()
#            t.text = topic.find(self.wp_ns + 'cat_name').text
#            t.slug = topic.find(self.wp_ns + 'category_nicename').text
#            if topic.find(self.wp_ns + 'category_parent').text:
#                t.parent = Topic.objects.get(slug=topic.find(self.wp_ns + 'category_parent').text)
#            t.save()
#
#    def import_posts(self):
#        '''Parses the Export File.'''
#        items = self.chan.findall('item')
#        for item in items:
#            self._import_post(item)
#
#    def _import_post(self, item):
#        '''Creates a new Entry object from a post and saves it.'''
#        wp_ns = self.wp_ns
#        content_ns = self.content_ns
#        if item.find(wp_ns + 'post_type').text == 'post':
#            post = Post()
#            post.author = self.get_author()
#            post.title = item.find('title').text
#            if not post.title:
#                post.title = 'ab origine' # Latin for 'from the source'
#            post.content = item.find(content_ns + 'encoded').text
#            if post.content:
#                post.content = post.content.replace("\n", "<br />")
#            post.teaser = item.find(self.excerpt_ns + 'encoded').text
#            # Parse wp:post_date in format 2002-02-27 13:39:00
#            postdate = datetime.strptime(item.find(wp_ns + 'post_date').text, "%Y-%m-%d %H:%M:%S")
#            post.pub_date = postdate
#            status = item.find(wp_ns + 'status').text
#            if status == 'publish':
#                post.status = 'P'
#            else:
#                post.status = 'U'
#            try:
#                post.save()
#
#                # modify date_created after save because autonow is on.
#                post.date_created = postdate
#                post.save()
#                # Enrich the rest of the post.
#                self._post_meta(post, item)
#                self._catalog_post(post, item)
#
#            except:
#                sys.stderr.write("Error importing %s" % post.title)
#                pass
#
#    def _post_meta(self, post, item):
#        '''Create Post Meta items.'''
#        wi = PostMeta(post=post, key='wp_post_id',
#                         value=item.find(self.wp_ns + 'post_id').text)
#        wi.save()
#        wbt = PostMeta(post=post, key='wp_blog_title',
#                                 value=self.chan.find('title').text)
#        wbt.save()
#        wl = PostMeta(post=post, key='wp_blog_link',
#                      value=self.chan.find('link').text)
#        wl.save()
#        wa = PostMeta(post=post, key='wp_author',
#                      value=item.find(self.dc_ns + 'creator').text)
#        wa.save()
#        # Construct the PostMeta information.
#        post_meta = item.findall(self.wp_ns + 'postmeta')
#        for meta in post_meta:
#            try:
#                pm = PostMeta()
#                pm.post = post
#                pm.key = meta.find(self.wp_ns + 'meta_key').text
#                pm.value = meta.find(self.wp_ns + 'meta_value').text[:255]
#                pm.save()
#            except: # @TODO change this to validation exception when 1.2 released.
#                sys.stderr.write("Unable to save %s %s for post %s. Skipping." % (pm.key, pm.value, post.title))
#                pass
#
#    def _catalog_post(self, post, item):
#        '''Build tags and topics for post.'''
#        post_cats = item.findall('category')
#        for pc in post_cats:
#            #check for attributes
#            if pc.get('nicename'):
#                if pc.attrib['domain'] == 'category':
#                    t = Topic.objects.get(slug=pc.attrib['nicename'])
#                    tc = TopicCatalog(content_object=post, topic=t)
#                    tc.save()
#                elif pc.attrib['domain'] == 'tag':
#                    t = Tag.objects.get(slug=pc.attrib['nicename'])
#                    tc = TaggedItem(content_object=post, tag=t)
#                    tc.save()
#