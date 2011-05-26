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

from django.http import Http404
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from metarho.blog.models import Post

def wp_post_redirect(view_fn):
    '''
    Checks a request for a querystring item matching a wordpress 
    post request.
    
    This is to enables url redirects for blog migrations from wordrpess.
    To use just decorate the view method for your default blog location.
    
    '''
    def decorator(request, *args, **kwargs):
        wp_query = request.GET.get('p', None)
        if wp_query:
            try:
                post = Post.objects.published().get(postmeta__key='wp_post_id', 
                                                    postmeta__value=wp_query)
                ar = post.pub_date.strftime("%Y/%b/%d").split('/')
                ar.append(post.slug)
                htr = HttpResponseRedirect(reverse('blog:post-detail', args=ar))
                htr.status_code = 301 # This should reflect a 'Moved Permanently' code.
                return htr
            except Post.DoesNotExist:
                raise Http404
        return view_fn(request, *args, **kwargs)

    return decorator