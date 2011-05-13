# file ontology/views.py
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

from django.shortcuts import get_object_or_404

from metarho import render_with_context
from metarho.ontology.models import Topic
from metarho.ontology.models import Tag

# Tag Related Stuff
def tags(request):
    """Returns a list of all tags for display and linking."""

    tags = Tag.objects.all()

    return render_with_context(request, 'ontology/tag_list.xhtml', {
            'title': 'All Tags',
            'description': "The following is a list of tags used for content.",
            'tags': tags,
            })

def tag(request, slug):
    """
    Returns a list of content related to a specific tag.

    :param slug: Tag slug to return content for.

    """
    tag = get_object_or_404(Tag, slug=slug)

    catalog = tag.taggeditem_set.all() # @TODO Change to published Only!!

    contentlist = [item for item in catalog if item.content_object.status == 'P']

    return render_with_context(request, 'ontology/tag_items.xhtml', {
        'title': "Items Under %s" % tag.text,
        'tag': tag,
        'contentlist': contentlist,
        })

# Topic Related Stuff
def topics(request):
    """Returns a list of all top level topics for display and linking."""

    topics = Topic.objects.filter(parent__isnull=True) # all top level topics.

    return render_with_context(request, 'ontology/topic_list.xhtml', {
            'title': 'All Topics',
            'description': "The following is a list of tags used for content.",
            'topics': topics,
            })

def topic(request, path):
    """
    Returns a list of content related to a specific topic.

    :param path: Topics path value.

    """
    pass