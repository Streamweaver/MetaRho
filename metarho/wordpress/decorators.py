# file decorators.py
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

from django.http import HttpResponsePermanentRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404
from django.core.urlresolvers import reverse

from metarho.wordpress.models import WPMapping
from metarho import PUBLISHED_STATUS

def wp_post_redirect(view_fn):
    '''
    Checks a request for a querystring item matching a wordpress 
    post request.
    
    This is to enables url redirects for blog migrations from wordrpess.
    To use just decorate the view method for your default blog location.
    
    '''
    def decorator(request, *args, **kwargs):
        id = request.GET.get('p', None)
        if id:
            item = get_object_or_404(WPMapping, wp_id=id)
            if item.post.status != PUBLISHED_STATUS:
                raise Http404
            post_args = {
                    'year': item.post.pub_date.year,
                    'month': item.post.pub_date.month,
                    'day': item.post.pub_date.day,
                    'slug': item.post.slug,
                }
            return HttpResponsePermanentRedirect(reverse('blog:post-detail', kwargs=post_args))
        return view_fn(request, *args, **kwargs)

    return decorator