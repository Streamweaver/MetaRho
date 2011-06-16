# file tests.py
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

"""
This file demonstrates two different styles of tests (one doctest and one
unittest). These will both pass when you run "manage.py test".

Replace these with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test import Client
from django.core.urlresolvers import reverse

class AuthTest(TestCase):
    """Test authentication methods."""
    
    fixtures = ['loremauth.json']

    def setUp(self):
        self.client = Client()

    def test_authenticate_user(self):
        fail_user = {'username': 'Octavian', 'password': 'killceasar'}
        response = self.client.post(reverse('account:login-form'), fail_user)
        expected = 1
        actual = len(response.context['auth_form'].errors)
        self.assertEqual(expected, actual, "FailUser did not raise error on login as expected. Expected %s; Raised: %s;" % (expected, actual))

        good_user = {'username': 'Julius', 'password': 'hailme'}
        response = self.client.post(reverse('account:login-form'), good_user)
        self.assertRedirects(response, reverse('account:index'))