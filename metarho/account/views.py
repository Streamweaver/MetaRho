# file views.py
#
# Copyright 2010, 2011 Scott Turnbull
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

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render
from django.shortcuts import HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required

def authenticate_user(request):
    """Logs a user into the application."""
    if request.user.is_authenticated():
        return HttpResponseRedirect(reverse('account:index'))
    auth_form = AuthenticationForm(None, request.POST or None)
    nextpage = request.GET.get('next', reverse('account:index'))
    msg = "Not Logged in"
    if auth_form.is_valid():
        login(request, auth_form.get_user())
        msg = 'Logged In'
        return HttpResponseRedirect(nextpage)
    return render(request, 'account/login.xhtml', {
        'auth_form': auth_form,
        'title': 'User Login',
        'next': nextpage,
        'message': msg,
    })

def logout_user(request):
    logout(request)
    return render(request, 'account/logout.xhtml', {})
    

@login_required
def profile(request):
    """For now it just renders the proper user in a template"""
    return render(request, 'account/profile.xhtml', {
        'user': request.user
    })