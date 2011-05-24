# file views.py
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

import datetime
import time

from django.http import Http404
from django.core.urlresolvers import reverse
from django.shortcuts import get_object_or_404

from metarho.blog.decorators import wp_post_redirect
from metarho.decorators import format_req
from metarho import render_with_context
from metarho.blog.models import Post
from metarho.blog.feeds import PostsFeedAtom
from metarho.blog.feeds import feed_render

# All Posts List Methods.
def post_all_feed(request):
    """Returns a Feed for all posts"""

    feed = PostsFeedAtom('myslug', request)
    feed.items = Post.objects.published().order_by('-pub_date')

    return feed_render(feed)

@wp_post_redirect
@format_req('rss', post_all_feed)
def post_all(request):
    """Returns all User Blogs"""
    posts = Post.objects.published()
    alt_links = [
    {'type': 'application/atom+xml', 'title': 'Atom Feed', 'href': '%s?format=rss' % reverse('blog:index')}
    ]
    
    return render_with_context(request, 'blog/post_list.xhtml', {
            'title': 'All Posts',                                                
            'posts': posts,
            'alt_links': alt_links,
            })

def post_year_feed(request, year):
    """Returns a Feed for particular year."""

    feed = PostsFeedAtom('myslug', request)
    feed.link = reverse('blog:list-year', args=[year])

    # Get the actual Items
    tt = time.strptime('-'.join([year]), '%Y')
    date = datetime.date(*tt[:3])
    feed.items = Post.objects.published().filter(pub_date__year=date.year).order_by('-pub_date')

    return feed_render(feed)

@format_req('rss', post_year_feed)
def post_year(request, year):
    """Returns all posts for a particular year."""
    tt = time.strptime('-'.join([year]), '%Y')
    date = datetime.date(*tt[:3])
    posts = Post.objects.published().filter(pub_date__year=date.year)
    
    return render_with_context(request, 'blog/post_list.xhtml', {
            'posts': posts,
            'title': 'Posts for %s' % date.strftime("%Y"),                                     
            })


def post_month_feed(request, year, month):
    """Returns an atom feed for the month."""
    feed = PostsFeedAtom('myslug', request)

    tt = time.strptime('-'.join([year, month]), '%Y-%b')
    date = datetime.date(*tt[:3])
    feed.items = Post.objects.published().filter(pub_date__year=date.year,
                            pub_date__month=date.month)

    return feed_render(feed)

@format_req('rss', post_month_feed)
def post_month(request, year, month):
    """Returns all posts for a particular month."""
    tt = time.strptime('-'.join([year, month]), '%Y-%b')
    date = datetime.date(*tt[:3])
    posts = Post.objects.published().filter(pub_date__year=date.year, 
                            pub_date__month=date.month)
    
    return render_with_context(request, 'blog/post_list.xhtml', {
            'posts': posts,
            'title': 'Posts for %s' % date.strftime("%B %Y"),                                     
            })

def post_day_feed(request, year, month, day):
    """Produces a feed for the post daily list."""

    feed = PostsFeedAtom('myslug', request)

    tt = time.strptime('-'.join([year, month, day]), '%Y-%b-%d')
    date = datetime.date(*tt[:3])
    feed.items = Post.objects.published().filter(pub_date__year=date.year,
                            pub_date__month=date.month, pub_date__day=date.day)

    return feed_render(feed)

@format_req('rss', post_day_feed)
def post_day(request, year, month, day):
    """Returns all posts for a particular day."""
    tt = time.strptime('-'.join([year, month, day]), '%Y-%b-%d')
    date = datetime.date(*tt[:3])
    posts = Post.objects.published().filter(pub_date__year=date.year, 
                            pub_date__month=date.month, pub_date__day=date.day)
    
    return render_with_context(request, 'blog/post_list.xhtml', {
            'posts': posts,
            'title': 'Posts for %s' % date.strftime("%A, %d %B %Y"),                                     
            })

# Detail Views
def post_detail(request, year, month, day, slug):
    """Returns an individual post."""
    tt = time.strptime('-'.join([year, month, day]), '%Y-%b-%d')
    date = datetime.date(*tt[:3])
    try:
        post = Post.objects.published().get(slug=slug, pub_date__year=date.year, 
                            pub_date__month=date.month, pub_date__day=date.day)
    except Post.DoesNotExist:
        raise Http404
    
    return render_with_context(request, 'blog/post_detail.xhtml', {
            'post': post,
            'title': post.title,                                     
            })

def archive_list(request):
    """Returns a list of months by year with published posts."""
    dates = Post.objects.published().order_by('pub_date').dates('pub_date', 'month')
    return render_with_context(request, 'blog/archive_list.xhtml', {
            'dates': dates,
            'title': 'Post Archive',
            })

# Views related to blogpost topics only.
def tag_list(request, slug):
    """Returns blog entries for this tag slug."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.published().filter(tags__tag__slug=slug)
    return render_with_context(request, 'blog/post_list.xhtml', {
        'posts': posts,
        'title': 'Posts tagged under %s' % tag.text,
        })