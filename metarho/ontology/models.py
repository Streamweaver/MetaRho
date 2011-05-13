# file ontology/models.py
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

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Tag(models.Model):
    '''
    Tags for blog entries that can cross relate information between users
    and categories.

    `Tags <http://en.wikipedia.org/wiki/Tag_%28metadata%29>`_ are intended to be
    single deapth way of quick way of catagorizing and relating content.

    '''

    text = models.CharField(max_length=30, unique=True)
    slug = models.SlugField(max_length=30, unique=True, null=True, blank=True)

    # Because I can't stop myself from adding these fields for some reason.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    def weight(self):
        """Returns the ratio this tag to total tags on items."""
        all_tags = TaggedItem.objects.all().count()
        this_tag = self.taggeditem_set.count()

        if all_tags == 0 or this_tag == 0: # make the return sensible
            return 0
        return this_tag/all_tags

    def save(self, force_insert=False, force_update=False):
        '''Extends the normal model save method to provide for slugs.'''

        # Create slug if none exists.
        if not self.slug:
            unique_slugify(self, self.text) # Create unique slug if none exists.

        super(Tag, self).save(force_insert, force_update) # Actual Save method.

    def __unicode__(self):
        return self.text

    class Meta:
        ordering = ['text']

class TaggedItem(models.Model):
    """
    Joining model between Tagged items and Tags.  I'm finding this more
    appealing both for performance issues and because tag slugs will be easier
    to maintain if Tags themselves are actually unique.
    
    """
    # What Tag is this referring to.
    tag = models.ForeignKey(Tag)
    # Content Type Stuff for generic relationships.
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return "%s" % self.tag.text

class Topic(models.Model):
    '''
    Topics provide `Catagorization <http://en.wikipedia.org/wiki/Categorization>`_
    of information in a hierarchal way.

    Topic slugs and names should be unque at it's level under Parent and the
    full name of a topic is considered the chained structure if itself and all
    it's parents.

    For instance a topic of "Django" under a parent topic of "Python" would be
    listed as "Python/Django" for it's display name and the path attribute would
    read as "python/django"

    '''
    text = models.CharField(max_length=75)
    parent = models.ForeignKey('self', null=True, blank=True) # Enable topic structures.
    description = models.TextField(null=True, blank=True)
    # Can be null and blank because it will get auto generated on save if so.
    slug = models.CharField(max_length=75, null=True, blank=True)
    path = models.CharField(max_length=255, blank=True)

    # Because I can't stop myself from adding these fields for some reason.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now_add=True, auto_now=True)

    def get_path(self):
        '''
        Constructs the path value for this topic based on hierarchy.

        '''
        ontology = []
        target = self.parent
        while(target is not None):
           ontology.append(target.slug)
           target = target.parent
        ontology.append(self.slug)
        return '%s/' % '/'.join(ontology) # Needs a trailing slash too.


    def save(self, force_insert=False, force_update=False):
        '''
        Custom save method to handle slugs and such.
        '''
        # Set pub_date if none exist and publish is true.
        if not self.slug:
            qs = Topic.objects.filter(parent=self.parent)
            unique_slugify(self, self.text, queryset=qs) # Unique for each parent.

        # Raise validation error if trying to create slug duplicate under parent.
        if Topic.objects.exclude(pk=self.pk).filter(parent=self.parent, slug=self.slug):
            raise ValidationError("Slugs cannot be duplicated under the same parent topic.")

        self.path = self.get_path() # Rebuild the path attribute whenever saved.

        super(Topic, self).save(force_insert, force_update) # Actual Save method.

    def __unicode__(self):
        '''Returns the name of the Topic as a it's chained relationship.'''
        ontology = []
        target = self.parent
        while(target is not None):
           ontology.append(target.text)
           target = target.parent
        ontology.append(self.text)
        return ' - '.join(ontology)

    class Meta:
        ordering = ['path']
        unique_together = (('slug', 'parent'), ('text', 'parent'))

class TopicCatalog(models.Model):
    """Joining model between Cataloged Models and Topics."""

    # Actual Topic this applies to.
    topic = models.ForeignKey(Topic)
    # Generic Content Type Items
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')