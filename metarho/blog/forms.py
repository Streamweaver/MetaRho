# file blog/forms.py
#
# Copyright 2011 Scott Turnbull
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

# Contains the various forms needed for managing and editing the blog app.

from django import forms

from metarho.blog.models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('title', 'author', 'status', 'tags', 'content', 'slug', 'teaser')
        exclude = ('pub_date',)

class ConfirmForm(forms.Form):
     confirm = forms.BooleanField(help_text="This cannot be undone!")