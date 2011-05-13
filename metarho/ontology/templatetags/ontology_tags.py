# file ontology/templatetags/ontology_tags.py
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

from django import template

from metarho.ontology.models import Tag
from metarho.ontology.models import TaggedItem

register = template.Library()

@register.inclusion_tag('ontology/snippets/tag_cloud.xhtml')
def tag_cloud():
    '''Produces a tag cloud of tags used in the database.'''
    tags = Tag.objects.order_by('text').filter(taggeditem__isnull=False)
    total = TaggedItem.objects.all().count()
    return {'tags': tags, 'total': total}