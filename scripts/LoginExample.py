import CustomTestCase

from pages.HomePage import HomePage

from nose.plugins.attrib import attr
from nose.plugins.skip import SkipTest

class LoginExample(CustomTestCase.CustomTestCase):
    @attr(tags=['deep', 'website', 'login', 'adam'])
    def incorrect_login(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_with_soft_assert(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.verifyEqual(l.error_message, "Incorrect username or password.")

    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_with_random_username_and_password(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        
        from generators.StringData import random_string
        l.username = random_string(5)
        l.password = random_string()
        
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_from_csv(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        
        from providers.csv_provider import CSVProvider
        p = CSVProvider('invalid_usernames.csv')
        data = p.randomRow()
        l.username = data['username']
        l.password = data['password']
        
        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")

    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_from_sqlite3(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()

        from providers.sqlite3_provider import DBProvider
        p = DBProvider()
        data = p.get_random_user()
        l.username = data['username']
        l.password = data['password']

        l.do_login()
        self.assertEqual(l.error_message, "Incorrect username or password.")
        
    @attr(tags=['deep', 'website', 'login'])
    def incorrect_login_fails(self):
        h = HomePage()
        h.open_default_url()
        l = h.go_to_login_page()
        l.username = "foo"
        l.password = "bar"
        l.do_login()
        self.assertEqual(l.error_message, "This message is deliberately incorrect to trigger a failed test.")