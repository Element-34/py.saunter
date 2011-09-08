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

from saunter.testcase.remotecontrol import SaunterTestCase

from pages.HomePage import HomePage

import pytest

class CheckLoginExample(SaunterTestCase):
    @pytest.marks('deep', 'sauce', 'login')
    def test_incorrect_login(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @pytest.marks('deep', 'sauce', 'login')
    def test_incorrect_login_with_soft_assert(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.verify_equal(l.error_message, "Incorrect username or password.")

    @pytest.marks('deep', 'sauce', 'login')
    def test_incorrect_login_with_random_username_and_password(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        
        from saunter.generators.string_data import random_string
        l.username = random_string(5)
        l.password = random_string()
        
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @pytest.marks('deep', 'sauce', 'login', 'csv')
    def test_incorrect_login_from_csv(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        
        from saunter.providers.csv_provider import CSVProvider
        p = CSVProvider('invalid_usernames.csv')
        data = p.randomRow()
        l.username = data['username']
        l.password = data['password']
        
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @pytest.marks('deep', 'sauce', 'login', "db")
    def test_incorrect_login_from_sqlite3(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()

        from providers.invalid_usernames import InvalidUsernames
        p = InvalidUsernames()
        data = p.get_random_user()
        l.username = data['username']
        l.password = data['password']

        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")
        
    @pytest.marks('deep', 'sauce', 'login')
    def test_incorrect_login_fails(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.assertEqual(l.error_message, "This message is deliberately incorrect to trigger a failed test.")