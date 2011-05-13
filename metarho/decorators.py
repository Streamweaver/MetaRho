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

# import mimeparse.py

MIME_TYPE = {
    'rss': ['application/rss+xml', 'text/xml'],
    'json': ['application/json', 'text/json'],
    'atom': ['application/atom+xml', 'text/xml'],
    'rdf': ['application/rdf+xml'],
    'html': ['text/html'],
}

FORMAT_MAP = {
    'html': 'text/html',
    'json': 'application/json',
    'xml': 'text/xml',
    'rss': 'application/rss+xml',
    'atom': 'application/atom+xml',
    'rdf': 'application/rdf+xml',
}

def format_req(fmt, new_fn):
    '''
    Provides compatability with URLs from things like wordpress that
    request content type via a querystring param like '?format=rss'

    :param fmt: String indicating format to return new_fn for.
    :param new_fn: Bound method to return if format querystring matches format.

    '''

    def _decorator(view_fn):
        def _wraped(request, *args, **kwargs):
            if request.GET.get('format', None) == fmt:
                return new_fn(request, *args, **kwargs)
            # Default to returning the original method
            return view_fn(request, *args, **kwargs)
        return _wraped
    return _decorator