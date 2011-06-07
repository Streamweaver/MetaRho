# file __init__.py
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

from optparse import make_option

from django.core.management.base import BaseCommand
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.models import User

from metarho.blog.importer import WordpressImporter

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
            make_option("-u", "--username", dest="username", default=None),
            make_option("-s", "--site", dest="site", default=None),
            make_option("-w", "--wordpressuser", dest="wordpressuser", default=None),
            make_option("-p", "--wordpresspw", dest="wordpresspw", default=None),
            make_option("-d", "--maxid", dest="maxid", default=None),
            make_option("-n", "--minid", dest="minid", default=1),
        )

    def handle(self, *args, **options):
        # Throws an error if not a valid user.
        user = self._get_user(options.get("username"))
        site = options.get("site")
        wp_user = options.get("wordpressuser")
        wp_pass = options.get("wordpresspw")
        max_id = options.get("maxid")
        min_id = options.get("minid")
        wp = WordpressImporter(site, wp_user, wp_pass, int(max_id), user, int(min_id))
        wp.import_all()
        
    def _get_user(self, username):
        """
        Returns user by `username` or throw an error saying they don't exist.

        :param username: Username of user to find or create.
        
        """
        try:
            return User.objects.get(username=username)
        except User.DoesNotExist:
            raise ObjectDoesNotExist('User %s does not exist!' % username)