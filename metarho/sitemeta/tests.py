# file sitemeta/tests.py
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

from django.test import TestCase
from django.contrib.auth.models import User
from django.contrib.sites.models import Site

from metarho.sitemeta.models import SiteInformation
from metarho.blog.importer import WordPressExportParser

class WordPressExportParserTest(TestCase):
    '''Tests the blog import scripts interaction with the sitemeta app only'''

    fixtures = ['loremauth.json',]

    def setUp(self):
        self.owner = User.objects.get(username='Julius')
        self.site = Site(domain='greatblogsite.com', name='Great Blog Site')
        self.site.save()
        file = 'blog/fixtures/wordpress.loremtest.xml'
        self.wp = WordPressExportParser(file, self.owner.username)

    def test_import_site_information(self):
        '''
        Not part of the blog app but is part of the parser this will fail if
        sitemeta is not in installed apps.

        '''
        self.wp.import_site_information()
        si = SiteInformation.objects.get(slug='streamweavers-blog')
        expected = 'Just another WordPress.com weblog'
        self.failUnlessEqual(expected, si.description, 'Expected description to read %s but returned %s' % (expected, si.description))
