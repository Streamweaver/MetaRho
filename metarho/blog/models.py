# file models.py
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

from datetime import datetime
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.core.exceptions import ValidationError
from django.contrib.contenttypes import generic

from metarho import PUBLISHED_STATUS
from metarho import PUB_STATUS
from metarho import unique_slugify

# Setup Other Apps to allow use without building strict dependencies.
from metarho.settings import INSTALLED_APPS
from metarho.settings import ENABLE_POST_TAGS

POST_TAGGING = False # Default to false unless it passes the settings test below.
if ENABLE_POST_TAGS and 'tagging' in INSTALLED_APPS:
    import tagging
    from tagging.fields import TagField
    POST_TAGGING = True # Set true to tell model imports are done and fields ready.

# CUSTOM MANAGERS

class PostManager(models.Manager):
    '''
    Adds some features to the default manager for published posts
    published dates.
    
    '''
    
    def published(self, pub_date=None):
        '''
        Only returns posts that are published and of pub_date or earlier.

        :param pub_date: Posts with pub_date later than this are not considered
                         published.

        '''
        if not pub_date:
            pub_date = datetime.now()
        return self.filter(status=PUBLISHED_STATUS, pub_date__lte=pub_date)
    
class Post(models.Model):
    '''Blog Entries'''

    title = models.CharField(max_length=75)
    slug = models.SlugField(max_length=75, blank=True, unique_for_date='pub_date')
    author = models.ForeignKey(User)
    content = models.TextField(null=True)
    teaser = models.TextField(null=True, blank=True)
    pd_help = 'Date to publish.'
    pub_date = models.DateTimeField(help_text=pd_help, blank=True, default=datetime.now, db_index=True)
    status = models.CharField(max_length=1, choices=PUB_STATUS)
    date_created = models.DateTimeField(null=False, blank=False, auto_now_add=True)
    date_modified = models.DateTimeField(null=False, blank=False, auto_now=True, auto_now_add=True)

    # If tagging for posts is enable and everything is setup right add the fields.
    if POST_TAGGING:
        tags = TagField(blank=True, null=True)

    objects = PostManager()

    @models.permalink
    def get_absolute_url(self):
        '''Get projects url.'''
        return reverse('blog:post-detail', args=[self.pub_date.year, date.strftime(self.pub_date, '%m'), date.strftime(self.pub_date, '%d'), self.slug])

    def __unicode__(self):
        return self.title
    
    def clean(self):
        '''
        Provide some custom validation and other tasks.
        
        '''
        # Set pub_date if none exist and publish is true.
        if not self.pub_date:
            self.pub_date = datetime.now() # No publishing without a pub_date
            
        # Create slug if none exists..
        if not self.slug:
            qs = Post.objects.all().filter(
                pub_date__year=self.pub_date.year,
                pub_date__month=self.pub_date.month,
                pub_date__day=self.pub_date.day
            )
            # Slug should be unique for date.
            unique_slugify(self, self.title, queryset=qs)

    def save(self, force_insert=False, force_update=False):
        '''
        Custom save method to handle slugs and such.
        @TODO Remove this once if using Django 1.2
        
        '''
        # @NOTE this is a work around until I go to django 1.2
        self.clean()
        super(Post, self).save(force_insert, force_update) # Actual Save method.

    class Meta:
        get_latest_by = 'pub_date'
        ordering = ['-pub_date']

class PostMeta(models.Model):
    '''Holds additional data in key:value pairs for posts.'''
    
    post = models.ForeignKey(Post)
    key = models.CharField(max_length=30, null=False, blank=False)
    value = models.CharField(max_length=255, null=False, blank=False)