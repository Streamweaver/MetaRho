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

from django.core.urlresolvers import reverse
from django.contrib.syndication.views import Feed
from django.utils import feedgenerator

from tagging.models import Tag

from metarho import user_name
from metarho.sitemeta.models import SiteInformation
from metarho.blog.models import Post


def _siteinfo():
    """Returns the default Site Information object."""
    return SiteInformation.objects.get(default=True)

class LatestPostsFeedRss(Feed):

    feed_type = feedgenerator.Rss201rev2Feed
    ttl = 600 # Hard-coded Time To Live.

    def title(self):
        """
        Returns the feed's title as a normal Python string.
        """
        return "Syndicated Feed of Posts for %s" % _siteinfo().title

    def link(self):
        """
        Returns the feed's link as a normal Python string.
        """
        return reverse('blog:index')

    def feed_guid(self):
        """
        Returns the feed's globally unique ID as a normal Python string.
        """
        return reverse('blog:index')

    def description(self):
        """
        Returns the feed's description as a normal Python string.
        """
        return _siteinfo().description

    def author_name(self):
        """
        Returns the feed's author's name as a normal Python string.
        """
        return user_name(_siteinfo().owner)

    def author_email(self):
        """
        Returns the feed's author's e-mail as a normal Python string.
        """
        return _siteinfo().owner.email

    def author_link(self):
        """
        Returns the feed's author's URL as a normal Python string.
        """
        return reverse('site-index')

    def categories(self):
        """
        Returns the feed's categories as iterable over strings.
        """
        return None

    def feed_copyright(self):
        """
        Returns the feed's copyright notice as a normal Python string.
        """
        return _siteinfo().copyright

    def items(self):
        """
        Returns a list of items to publish in this feed.
        """
        return Post.objects.published()[:10]

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
        return reverse('blog:post-detail', args=[item.pub_date.year, item.pub_date.strftime('%m'), item.pub_date.day, item.slug])

    def item_author_name(self, item):
        """
        Takes an item, as returned by items(), and returns the item's
        author's name as a normal Python string.
        """
        return user_name(item.author)

    def item_author_email(self, obj):
        """
        Takes an item, as returned by items(), and returns the item's
        author's e-mail as a normal Python string.
        """
        return obj.author.email

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
        tags = [tag.name for tag in Tag.objects.get_for_object(item)]
        return tags

    def item_copyright(self):
        """
        Returns the copyright notice for every item in the feed.
        """
        return _siteinfo().copyright

class LatestPostsFeedAtom(LatestPostsFeedRss):

    feed_type = feedgenerator.Atom1Feed

    def subtitle(self):
        return self.description()
