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
import unicodedata
from datetime import datetime


from metarho.blog.models import Post

import pprint

class WordpressImporter:

    error_ids = []
    success_ids = []

    def __init__(self, url, user, pw, maxid, author, minid=1):
        """Initializes a new wp importer """
        self.blog = pyblog.WordPress(url, user, pw)
        self.id_range = range(minid, maxid)
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
        print "DONE! Imported %s and skipped %s" % (len(self.success_ids), len(self.error_ids))

    def import_post(self, wp_post):
        # 'From Twitter 'in title
        # 'LoudTwitter'
        if re.search('From Twitter ', wp_post['title']):
            print "Skipping tittinisis post %s" % wp_post['title']
            return True
        if re.search('LoudTwitter', wp_post['description']):
            print "Skipping loudtwitter post %s" % wp_post['title']
            return True
        post = Post()
        post.title = self._title_parse(wp_post["title"])
        post.content = self._content_normalize(wp_post['description'])
        post.slug = self._slug_check(wp_post['wp_slug'])
        post.pub_date = datetime.strptime(str(wp_post['dateCreated']), "%Y%m%dT%H:%M:%S")
        post.author = self.author
        post.status = 'U'
        if wp_post['post_status'] == 'publish':
            post.status = 'P'
        post.save() # Set date created/modified so I can change them.
        post.date_created = datetime.strptime(str(wp_post['dateCreated']), "%Y%m%dT%H:%M:%S")
        post.save()

    def _title_parse(self, title):
        """Fix title format problems with import."""
        if not title: # Default to this title if blank
            return "No Title"
        if len(title) > 75: # Truncate and format title if it's too long
            return "%s..." % title[0:71]
        return title # Otherwise return the title normally

    def _slug_check(self, slug):
        """Deal with slugs that are too large."""
        if len(slug) > 75:
            return None # Null out the slug and the model will just rebuild it based on title.
        return slug # Pass through returns slug normally

    def _content_normalize(self, content):
        """Fix problems witih some content having stray unicode"""
        try:
            return unicodedata.normalize('NFKD', content)
        except TypeError:
            return content

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


