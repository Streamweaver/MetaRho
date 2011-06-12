# file blog/tests.py
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

from datetime import datetime
from datetime import date
from datetime import timedelta

from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.test.client import Client

from metarho.blog.models import Post
#from metarho.blog.importer import WordPressExportParser
#from metarho.ontology.models import Tag
#from metarho.ontology.models import Topic

# CUSTOM MANAGER TESTS

class PostManagerTest(TestCase):
    '''Tests methods related to the custom post manager.'''
    
    fixtures = ['loremauth.json', 'loremblog.json']
    
    def setUp(self):
        # Define a default users.
        self.author = User(username='Fakeuser', email='fakeuser@email.com')
        self.author.save()
    
    def test_published(self):
        '''Tests that only published posts are returned.'''
        actual = Post.objects.all().count()
        expected = 4 # 3 total posts of all status
        self.failUnlessEqual(expected, actual, 'Expected %s posts and returned %s!' % (expected, actual))

        actual = Post.objects.published().count()
        expected = 2 # Only one published.
        self.failUnlessEqual(expected, actual, 'Expected %s posts and returned %s!' % (expected, actual))

        # Create a new post with a future publish date
        p = Post(title='test', content='test', status='P')
        p.author = self.author
        p.save()
        actual = Post.objects.published().count()
        expected = 3 # Pubdate defaults to now.
        self.failUnlessEqual(expected, actual, 'Expected %s posts and returned %s!' % (expected, actual))

        p.pub_date = datetime.now() + timedelta(days=1)
        p.save()
        actual = Post.objects.published().count()
        expected = 2 # Should now be 1 with postdated pub_date.
        self.failUnlessEqual(expected, actual, 'Expected %s posts and returned %s!' % (expected, actual))

class ModelPostTest(TestCase):

    fixtures = ['loremauth.json', 'loremblog.json']

    def test_save(self):
        """Tests the custom save method."""
        
        user = User(username='Fakeuser', password='notgood', email='fakeuser@email.com')
        user.save()
        
        user2 = User(username='Fakeuser2', password='notgoodeither', email='fu2@email.com')
        user2.save()
        
        p = {
             'title': 'Test Title (1)',
             'author': user,
             'content': 'some content',
             'status': 'U'
             }
        
        post1 = Post(**p)
        post1.save()

        slugexp = 'test-title-1' 
        slugact = post1.slug
        self.failUnlessEqual(slugexp, slugact, 'Slug was %s but expected %s' % (slugact, slugact))
        self.failUnless(post1.pub_date, 'Post1 pub_date was not set!')
 
        # Set the pub_date back to setup next test.
        new_date = datetime.now() - timedelta(days=1) - timedelta(hours=2)
        post1.pub_date = new_date
        post1.save()
        
        # Setup another post with old pubdate, then change to now to see what happens.
        # Test some slug collisions and such.
        p2 = p.copy()
        p2['status'] = 'P'
        post2 = Post(**p2)
        post2.save()
        
        # Test the slugify feature
        slug = 'test-title-1' 
        self.failUnlessEqual(slug, post2.slug, 'Post2 slug was %s but expected %s' % (post2.slug, slug))
 
        # Set date on post 2 to the same to test unique slugify feature
        post2.pub_date = datetime.now() - timedelta(days=1) - timedelta(hours=1)

        # Test the auto-increment feature of the unique_slugify method.
        post2.slug = None
        post2.save()
        expected = 'test-title-1-2'
        self.failUnlessEqual(post2.slug, expected, 'Post2 slug was %s but expected %s' % (post2.slug, expected))

class ViewTest(TestCase):
    '''
    Tests the various views returned  by the app.
    
    user:  Julius
    pw: hailme
    email: ceasar@rome.org
    
    '''
    
    fixtures = ['loremauth.json', 'loremblog.json']
    
    def setUp(self):
        self.client = Client()
    
    def test_post_detail(self):
        '''Tests individual entry return.'''
        # Fetch All Posts and make sure they work as expected.
        expected = {'P': 200, 'U': 404}
        posts = Post.objects.all()
        for post in posts:
            attrs = [post.pub_date.year, date.strftime(post.pub_date, '%m'), post.pub_date.day, post.slug]
            url = reverse('blog:post-detail', args=attrs)
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected[post.status], code, 'Expected %s but returned %s for %s' % (expected[post.status], code, url))

    def test_post_detail_alt(self):
        '''Tests individual entry return with alt urls.'''
        # Fetch All Posts and make sure they work as expected.
        expected = {'P': 200, 'U': 404}
        posts = Post.objects.all()
        for post in posts:
            attrs = [post.pub_date.year, date.strftime(post.pub_date, '%b'), post.pub_date.day, post.slug]
            url = reverse('blog:post-detail-alt', args=attrs)
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected[post.status], code, 'Expected %s but returned %s for %s' % (expected[post.status], code, url))

    def test_wp_redirect(self):
        '''
        Tests the wp_post_redirect decorator.
        
        '''
        expected = 301
        url = '?p=4'
        code = self.client.get(url).status_code
        self.failUnlessEqual(code, expected, 'Expected %s but returned %s for %s' % (expected, code, url))
        
    def test_post_all(self):
        '''Tests the default return of posts.'''
        url = reverse('blog:index')
        code = self.client.get(url).status_code
        expected = 200
        self.failUnlessEqual(code, expected, 'Expected %s but returned %s for %s' % (expected, code, url))

    def test_post_year(self):
        '''Tests the return of year archives.'''
        posts = Post.objects.published()
        for post in posts:
            expected = 200
            url = reverse('blog:list-year', args=[post.pub_date.year])
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected, code, 'Expected %s but returned %s for %s' % (expected, code, url))

    def test_post_month(self):
        '''Tests the return of month archives.'''
        posts = Post.objects.published()
        for post in posts:
            expected = 200
            url = reverse('blog:list-month', args=[post.pub_date.year, date.strftime(post.pub_date, '%m')])
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected, code, 'Expected %s but returned %s for %s' % (expected, code, url))

    def test_post_month_alt(self):
        '''Tests the return of month archives.'''
        posts = Post.objects.published()
        for post in posts:
            # Test Normally.  i.e. 'mar'
            expected = 200
            month = date.strftime(post.pub_date, '%b')
            url = reverse('blog:list-month-alt', args=[post.pub_date.year, month])
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected, code, 'Expected %s but returned %s for %s' % (expected, code, url))
            # Test title case.  i.e. 'Mar'
            url = reverse('blog:list-month-alt', args=[post.pub_date.year, month.capitalize()])
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected, code, 'Expected %s but returned %s for %s' % (expected, code, url))
            # Test uppercase.  i.e. 'MAR'
            url = reverse('blog:list-month-alt', args=[post.pub_date.year, month.upper()])
            code = self.client.get(url).status_code
            self.failUnlessEqual(expected, code, 'Expected %s but returned %s for %s' % (expected, code, url))

    def test_post_day(self):
        '''Tests the return for a post day list.'''
        attrs = ['2009', '04', '08']
        url = reverse('blog:list-day', args=attrs)
        expected = 200
        code = self.client.get(url).status_code
        self.failUnlessEqual(code, expected, 'Expected %s but returned %s for %s' % (expected, code, url))

        # Test an unpublished one.
        attrs = ['2010', '03', '23']
        url = reverse('blog:list-day', args=attrs)
        expected = 1 # There are 2 but 1 is unpublished.
        response = self.client.get(url)
        posts = len(response.context['post_list'])
        self.failUnlessEqual(posts, expected, 'Expected %s posts but returned %s for %s' % (expected, posts, url))

    def test_post_day_alt(self):
        '''Test return of posts on a day through alt view.'''
        attrs_list = (['2010', 'mar', '23'], ['2010', 'Mar', '23'], ['2010', 'MAR', '23'])
        expected = 1 # There are 2 but 1 is unpublished.
        for attrs in attrs_list:
            url = reverse('blog:list-day-alt', args=attrs)
            response = self.client.get(url)
            posts = len(response.context['post_list'])
            self.failUnlessEqual(posts, expected, 'Expected %s posts but returned %s for %s' % (expected, posts, url))