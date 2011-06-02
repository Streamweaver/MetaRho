# file settings.py
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
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS

from os import path

# Get the directory of this file for relative dir paths.
# Django sets too many absolute paths.
BASE_DIR = path.dirname(path.abspath(__file__))

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'utf-8'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale
USE_L10N = True

# URL prefix for admin static files -- CSS, JavaScript and images.
# Make sure to use a trailing slash.
# Examples: "http://foo.com/static/admin/", "/static/admin/".
ADMIN_MEDIA_PREFIX = '/sitemedia/admin/'

# Absolute path to the directory that holds sitemedia.
# Example: "/home/sitemedia/sitemedia.lawrence.com/"
MEDIA_ROOT = path.join(BASE_DIR, 'sitemedia/'),

# URL that handles the sitemedia served from MEDIA_ROOT. Make sure to use a
# trailing slash if there is a path component (optional in other cases).
# Examples: "http://sitemedia.lawrence.com", "http://example.com/sitemedia/"
MEDIA_URL = '/sitemedia'

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/sitemedia/sitemedia.lawrence.com/static/"
STATIC_ROOT =  path.join(BASE_DIR, 'collectedmedia/')

# URL prefix for static files.
# Example: "http://sitemedia.lawrence.com/static/"
STATIC_URL = '/sitemedia/'

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(BASE_DIR, 'sitemedia'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
#     'django.template.loaders.eggs.load_template_source',
)

TEMPLATE_CONTEXT_PROCESSORS = TEMPLATE_CONTEXT_PROCESSORS + (
    "django.core.context_processors.request",
)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'pagination.middleware.PaginationMiddleware',
)

ROOT_URLCONF = 'metarho.urls'

TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    path.join(BASE_DIR, 'templates'),
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'django.contrib.staticfiles',
    'metarho.account',
    'metarho.sitemeta',
    'metarho.blog',
    'south', # Depends on south migrations for managing schemas.
    'tagging', # Comment out if not using Django Tagging.
    'pagination',
)

# Set to TRUE to including tagging in posts.
ENABLE_POST_TAGS = True
FORCE_LOWERCASE_TAGS = True # Override setting in tagging module.

# Django Pagination Settings
# PAGINATION_DEFAULT_PAGINATION = 1
# The default amount of items to show on a page if no number is specified.

#PAGINATION_DEFAULT_WINDOW = 3
# The number of items to the left and to the right of the current page to display (accounting for ellipses).

#PAGINATION_DEFAULT_ORPHANS = 0
# The number of orphans allowed. According to the Django documentation, orphans are defined as:
# The minimum number of items allowed on the last page, defaults to zero.

PAGINATION_INVALID_PAGE_RAISES_404 = True
# Determines whether an invalid page raises an Http404 or just sets the invalid_page context variable.
# True does the former and False does the latter.

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}

try:
    from localsettings import *
except ImportError:
    import sys
    print >>sys.stderr, '''Settings not defined.  Please configure a version of
    localsettings.py for this site.  See localsettings-dist.py for setup
    details.'''
    del sys
