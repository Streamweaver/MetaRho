# file sitemeta/models.py
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
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from metarho import unique_slugify

SITE_CACHE = {}

class SiteInformation(models.Model):
    '''
    This sets information about the site in general terms and provides defaults
    for use throughout the site.

    @TODO Set this information in the site cache for better performance.
    
    '''
    title = models.CharField(max_length=75)
    site = models.ForeignKey(Site, help_text='Which Site is this  related to?')
    # Probably not needed but I feel compelled.
    slug = models.SlugField(max_length=75, unique=True, blank=True)
    owner = models.ForeignKey(User, help_text='Who to contact and credit')
    default = models.BooleanField(default=True, help_text='Is this the default config to use?')
    description = models.TextField(null=True, blank=True, help_text='Tagline or overall summary.')
    copyright = models.TextField(null=True, blank=True, help_text='Default copyright to use for site content.')
    # Not sure why but I always feel compelled to add these two fields.
    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        '''Return the site title.'''
        return self.title

    def save(self, force_insert=False, force_update=False):
        '''Custom save method performs some needed juggling of the object.'''

        # Make sure cached info is synced with current state of the object.
        if self.pk in SITE_CACHE:
            del SITE_CACHE[self.pk]

        if self.default: # Make sure there is only one default site information.
            SiteInformation.objects.all().update(default=False)

        if not self.slug: # Autogenerate a slug if one isn't provided.
             unique_slugify(self, self.title)
        super(SiteInformation, self).save(force_insert, force_update)

    def delete(self):
        """Delete needs to interact with cache as well."""
        super(Site, self).delete()
        if self.pk in SITE_CACHE:
            del SITE_CACHE[self.pk]