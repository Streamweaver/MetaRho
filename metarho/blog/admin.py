# file blog/admin.py
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

# Admin classes for blog models
from metarho.blog.models import Post
from metarho.blog.models import PostMeta

from django.contrib import admin
from django.db import models
from django import forms
from django.conf import settings

media = settings.MEDIA_URL

class PostMetaInline(admin.TabularInline):
    model = PostMeta

class PostAdmin(admin.ModelAdmin):
    '''
    Admin interface options for the Post model.
    '''
    search_fields = ['title']
    list_display = ('title', 'status')
    list_filter = ('status', 'pub_date', 'author', 'topics')
    inlines = [PostMetaInline,]
    formfield_overrides = { models.TextField: {'widget': forms.Textarea(attrs={'class':'tinymce'})}, }
    
    class Media:
        js = (
              'http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js',
              ''.join([media, '/js/tinymce/jscripts/tiny_mce/jquery.tinymce.js']),
              )
    
admin.site.register(Post, PostAdmin)
