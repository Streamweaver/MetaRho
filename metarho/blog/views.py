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
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import permission_required
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from tagging.models import Tag
from tagging.models import TaggedItem

from metarho import PUBLISHED_STATUS
from metarho import PUB_STATUS
from metarho import unique_slugify
from metarho.blog.decorators import wp_post_redirect
from metarho.decorators import format_req
from metarho.blog.models import Post
from metarho.blog.feeds import PostsFeedAtom
from metarho.blog.feeds import feed_render
from metarho.blog.forms import PostForm
from metarho.blog.forms import ConfirmForm

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
    
    return render(request, 'blog/post_list.xhtml', {
            'title': 'All Posts',                                                
            'post_list': posts,
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
    
    return render(request, 'blog/post_list.xhtml', {
            'post_list': posts,
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
    
    return render(request, 'blog/post_list.xhtml', {
            'post_list': posts,
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
    
    return render(request, 'blog/post_list.xhtml', {
            'post_list': posts,
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
    
    return render(request, 'blog/post_detail.xhtml', {
            'post': post,
            'title': post.title,                                     
            })

# Post Admin views
@login_required
def post_edit(request, id=None):
    """
        Handles creating or updating of individual blog posts.

        :parm request: request object being sent to the view.
        :param id: post id, defaults to None if new post.
        
       """
    instance = None
    if id:
        instance = get_object_or_404(Post, id=id)

    title = "Create New Post"
    if instance:
        title = "Editing Post"

    # Create the form as needed.
    form = PostForm(request.POST or None, instance=instance)

    # Save the edited form if needed
    if request.method == 'POST' and form.is_valid():
        tmp_form = form.save(commit=False)
        # Set author to current user if none set.
        if not tmp_form.author:
            tmp_form.author = request.user.id
        # Set pub_date if none exist and post is published.
        if tmp_form.status == PUBLISHED_STATUS and not tmp_form.pub_date:
            tmp_form.pub_date = datetime.now()
        tmp_form.save()
        return HttpResponseRedirect(reverse('blog:post-edit', args=[tmp_form.id]))
        
    return render(request, 'blog/post_edit.xhtml', {
        'title': title,
        'form': form,
    })

@login_required
@permission_required('blog.delete_post')
def post_delete(request, id):
    """Deletes a post."""
    
    deleted = False # No success by default
    post = get_object_or_404(Post, id=id) # Find the post or 404
    form = ConfirmForm(request.POST or None) # Bind the form to post or deliver a fresh one.
    if request.method == 'POST' and form.is_valid():
        post.delete()
        deleted = True # If post was deleted set to true to display the right message.
    return render(request, 'blog/post_delete.xhtml', {
        'title': 'Confirm Post Delete?',
        'form': form,
        'deleted': deleted,
    })

# Archive views of posts.

def archive_list(request):
    """Returns a list of months by year with published posts."""
    dates = Post.objects.published().order_by('pub_date').dates('pub_date', 'month')
    return render(request, 'blog/archive_list.xhtml', {
            'dates': dates,
            'title': 'Post Archive',
            })

# Views related to blogpost topics only.
def tag_list(request, slug):
    """Returns blog entries for this tag slug."""
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.published().filter(tags__tag__slug=slug)
    return render(request, 'blog/post_list.xhtml', {
        'post_list': posts,
        'title': 'Posts tagged under %s' % tag.text,
        })

def post_list_bytag(request, tagname):
    """Returns a list of Posts tagged with 'tagname'"""
    tag = get_object_or_404(Tag, name=tagname)
    post_list = TaggedItem.objects.get_by_model(Post, tag)
    return render(request, 'blog/post_list.xhtml', {
        'title': 'Posts tagged under <em>%s</em>' % tagname,
        'post_list': post_list,

    })

def tag_list(request):
    """Lists all tags."""
    tag_list = Tag.objects.usage_for_model(Post, counts=True)
    return render(request, 'blog/tag_list.xhtml', {
        'title': 'All Tags on Posts',
        'tag_list': tag_list,
    })