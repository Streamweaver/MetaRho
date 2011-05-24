# file feeds.py
#
# Copyright 2010 Scott Turnbull
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from datetime import date

from django.http import Http404
from django.http import HttpResponse
from django.contrib.syndication import feeds
from django.utils import feedgenerator
from django.core.urlresolvers import reverse
# from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404

from metarho.sitemeta.models import SiteInformation

def feed_render(feed):
    '''
    Creates a Feed and returns it as an HttpResponse or throws an error.
    
    :parm feed: Feed object to attempt to render.
    
    '''
    try: # Try to create the feed or throw an error if it doesn't exist.
        feedgen =feed.get_feed('')
    except feeds.FeedDoesNotExist:
        raise Http404, 'Invalid parameters.  A feed exists for %s but the parameters passed are incorrect.' % feed.link

    # Good to Go!  Create the feed as a response.
    response = HttpResponse(mimetype=feedgen.mime_type)
    feedgen.write(response, 'utf-8')
    return response

class PostsFeed(feeds.Feed):
    '''
    Returns the latests posts in RSS format.
    
    Each atrribute has alternate ways they can be called in a feed.  See 
    `Django Syndication Famework 
    <http://docs.djangoproject.com/en/dev/ref/contrib/syndication/>`_ for more 
    information.
    
    '''

    feed_type = feedgenerator.Rss201rev2Feed

    # These have alternate ways they can be called in a feed.  See `Django
    # Syndication Famework <http://docs.djangoproject.com/en/dev/ref/contrib/syndication/>`
    items = None
    ttl = 600 # Hard-coded Time To Live.

    def get_object(self, bits):
        '''
        Sets the main publication for the feed to pull general feed
        information from.

        '''
        return get_object_or_404(SiteInformation, default__exact=True)

    def title(self, obj):
        '''Returns the title of the publication.'''
        return obj.title

    def description(self, obj):
        '''Returns the description of the publication.'''
        return obj.description

    def link(self):
        return "test link"

    def author_name(self, obj):
        '''Returns the publication owners name.'''
        if obj.owner.get_full_name():
            obj.owner.get_full_name()
        return obj.owner.username

    def author_email(self, obj):
        '''Returns the publication owners email.'''
        return obj.owner.email

    def author_link(self, obj):
        '''
        Returns the publication owners profile page.
        
        '''
        # @TODO Change this to user profile page once it exists.
        return reverse('blog:index')

    def feed_copyright(self):
        '''Generates the Copyright Statement for the Feed.'''

        statement = """
        Copyright (c) 2001 - %s Flagon With The Dragon.

        Except where otherwise noted Creative Commons Attribution
        Non-Commercial Share Alike 3.0 License.
        """  % (date.today().year,)

        return statement

    def item_copyright(self, item):
        '''Returns Individual Item Copyright Statements.'''

        statement = """
        Copyright (c) %s Flagon With The Dragon.

        Except where otherwise noted Creative Commons Attribution
        Non-Commercial Share Alike 3.0 License.
        """  % (item.pub_date.year,)

        return statement

    def item_title(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        title as a normal Python string.
        
        """
        return item.title

    def item_description(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        description as a normal Python string.

        """
        return item.content

    def item_link(self, item):
        """
        Takes an item, as returned by items(), and returns the item's URL.
        
        """
        return reverse('blog:post-detail', args=[item.pub_date.year, item.pub_date.strftime('%b'), item.pub_date.day, item.slug])
    
    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        name = item.author.username
        if item.author.get_full_name():
            name = item.author.get_full_name()
        return name

    def item_author_email(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        author's e-mail as a normal Python string.
        
        """
        return obj.author.email

    def item_author_link(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        author's URL as a normal Python string.

        """
        # @TODO Make this link to userprofile when available.
        return reverse('blog:index')

    def item_pubdate(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        pubdate.

        """
        return item.pub_date

    def item_categories(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        categories.
        
        """
        cats = [topic.text for topic in item.topics.published()]
        return cats.extend([tag.text for tag in item.tags.published()])

class PostsFeedAtom(PostsFeed):

    feed_type = feedgenerator.Atom1Feed

    def subtitle(self):
        return self.description(self.get_object(''))