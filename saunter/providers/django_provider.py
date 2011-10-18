# Copyright 2011 Element 34
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""
===============
django_provider
===============
"""
import os
import sys
import saunter.ConfigWrapper

class DjangoProvider(object):
    """
    Uses Django's Models to access the database
    """
    def __init__(self):
        cf = saunter.ConfigWrapper.ConfigWrapper().config
        django_where = cf.get("Django", "installation")
        if django_where not in sys.path:
            sys.path.append(django_where)

        django_name = cf.get("Django", "app")
        if not 'DJANGO_SETTINGS_MODULE' in os.environ:
            os.environ['DJANGO_SETTINGS_MODULE'] = "%s.settings" % django_name

    def get_random_user(self):
        """
        Gets a random user from the provider

        :returns: Dictionary
        """
        from provider.models import User
        u = User.objects.order_by('?')[0]
        return {"username": u.username, "password": u.password, "fullname": u.fullname}