"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase

from metarho.wordpress.models import WPMapping
from metarho import PUBLISHED_STATUS, UNPUBLISHED_STATUS

class WPPostRedirectTest(TestCase):
    fixtures = ['loremauth.json', 'loremblog_0006.json', 'loremsitemeta.json', 'loremwp.json']

    def test_wp_redirect(self):
        '''
        Tests the wp_post_redirect decorator.

        '''
        item_list = WPMapping.objects.all()
        for item in item_list:
            url = "/?p=%s" % item.wp_id
            code = self.client.get(url).status_code
            expected = {UNPUBLISHED_STATUS: 404, PUBLISHED_STATUS: 301} # Unpublished should give 404 and Published a permanent redirect 301
            self.failUnlessEqual(code, expected[item.post.status], 'Expected %s but returned %s for %s' % (expected[item.post.status], code, url))
