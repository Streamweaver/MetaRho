# file ontology/tests.py
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

# @NOTE: Most tests involving the generic relations are conducted in the
# application relating to these models instead of here since the implementation
# is more aptly tested there than here.  Tests here covers only functionality
# completely encapsulated in this application.

from metarho.ontology.models import Tag
from metarho.ontology.models import Topic

class TagTest(TestCase):
    '''Tag Model tests.'''
    def test_save(self):
        '''Just testing that autoslugify works.'''
        tag = Tag(text='Test Me 2/ See IF it (works)')
        tag.save()
        expected = 'test-me-2-see-if-it-works'
        actual = tag.slug
        self.failUnlessEqual(expected, actual, 'Expected %s but slug was %s'% (expected, actual))

class TopicTest(TestCase):
    '''Topic Model tests.'''
    def test_save(self):
        '''Make sure slugify works and is unique only per parent.'''

        # Parent tests basic slug creation.
        parent = Topic(text='Parent')
        parent.save()
        expected = 'parent'
        actual = parent.slug
        self.failUnlessEqual(expected, actual, 'Parent slug was %s but expected %s' % (actual, expected))

        # Child tests slug with parent.
        child = Topic(text='Child', parent=parent)
        child.save()
        expected = 'child'
        actual = child.slug
        self.failUnlessEqual(actual, expected, 'Child slug was %s but expected %s' % (actual, expected))

        # Child2 tests slug with same name under same parent.
        child2 = Topic(text='Child', parent=parent)
        try:
            child2.save()
            result = False
        except:
            result = True
        self.assertTrue(result, "Unique Together attribute of Topic failed.")

        # Try one with different parent name but same child name as another parent.
        parent2 = Topic(text='Parent2')
        parent2.save()
        child3 = Topic(text='Child', parent=parent2)
        child3.save()
        expected = 'child'
        actual = child3.slug
        self.failUnlessEqual(actual, expected, 'Child3 slug was %s but expected %s' % (actual, expected))
