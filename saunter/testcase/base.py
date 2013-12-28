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

import time
import urllib2
import os
import os.path
import saunter.matchers as matchers


class BaseTestCase(object):
    def assertEqual(self, first, second, msg=None):
        self.matchers.assert_equal(first, second, msg)

    def assertNotEqual(self, first, second, msg=None):
        self.matchers.assert_not_equal(first, second, msg)

    def assertTrue(self, expr, msg=None):
        self.matchers.assert_true(expr, msg)

    def assertFalse(self, expr, msg=None):
        self.matchers.assert_false(expr, msg)

    def assertIs(self, first, second, msg=None):
        self.matchers.assert_is(first, second, msg)

    def assertIsNot(self, first, second, msg=None):
        self.matchers.assert_is_not(first, second, msg)

    def assertIsNone(self, expr, msg=None):
        self.matchers.assert_is_none(expr, msg)

    def assertIsNotNone(self, expr, msg=None):
        self.matchers.assert_is_not_none(expr, msg)

    def assertIn(self, first, second, msg=None):
        self.matchers.assert_in(first, second, msg)

    def assertNotIn(self, first, second, msg=None):
        self.matchers.assert_not_in(first, second, msg)

    def assertIsInstance(self, obj, cls, msg=None):
        self.matchers.assert_is_instance(obj, cls, msg)

    def assertIsNotInstance(self, obj, cls, msg=None):
        self.matchers.assert_is_not_instance(obj, cls, msg)

    def _screenshot_prep_dirs(self):
        class_dir = os.path.join(os.path.join(self.config['saunter']['log_dir'], self.__class__.__name__))
        if not os.path.exists(class_dir):
            os.makedirs(class_dir)

        method_dir = os.path.join(class_dir, self.current_method_name)
        if not os.path.exists(method_dir):
            os.makedirs(method_dir)

        return method_dir
