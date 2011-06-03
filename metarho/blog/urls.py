# file blog/urls.py
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

from django.conf.urls.defaults import *

from metarho.blog.feeds import LatestPostsFeedAtom

urlpatterns = patterns('metarho.blog.views',
    # Alt links are from a previous pattern I used for a bit using 3 char month abbreviation.
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/(?P<slug>[0-9A-Za-z-]+)/$', 'post_detail_alt'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', 'post_day_alt'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$', 'post_month_alt'),
    # Two digit for month is now the standard format.
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>[0-9A-Za-z-]+)/$', 'post_detail', name='post-detail'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', 'post_day', name='list-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$', 'post_month', name='list-month'),
    url(r'^(?P<year>\d{4})/$', 'post_year', name='list-year'),
    url(r'^archive/$', 'archive_list', name='archive-list'),
    url(r'^create/$', 'post_edit', name='post-create'),
    url(r'^edit/(?P<id>[0-9]+)/$', 'post_edit', name='post-edit'),
    url(r'^delete/(?P<id>[0-9]+)/$', 'post_delete', name='post-delete'),
    url(r'^tag/$', 'tag_list', name='tag-list'),
    url(r'^tag/(?P<tagname>[^/]+)/$', 'post_list_bytag', name='tag-post-list'),
    url(r'^feed/$', LatestPostsFeedAtom(), name='feed'),
    url(r'^switchmobile/$', 'mobile_switcher', name='switch-mobile'),
    url(r'^/$', 'post_all', name='index'),
)