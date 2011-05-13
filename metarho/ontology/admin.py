# file ontology/admin.py
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

from django.contrib import admin

from metarho.ontology.models import Tag
from metarho.ontology.models import Topic

class TagAdmin(admin.ModelAdmin):
    search_fields = ['text']

class TopicAdmin(admin.ModelAdmin):
    search_fields = ['text']


admin.site.register(Tag, TagAdmin)
admin.site.register(Topic, TopicAdmin)