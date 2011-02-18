import unittest2 as unittest

import logging

from pages.login_page import LoginPage
from SeleniumWrapper import SeleniumWrapper as wrapper
from providers.LoginProviders import StaticProvider

import ConfigWrapper
import string
import random

class CustomTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.cf = ConfigWrapper.ConfigWrapper().config
        self.selenium = wrapper().connect(self.cf.get("Selenium", "server_host"), \
                                          self.cf.get("Selenium", "server_port"), \
                                          self.cf.get("Selenium", "browser"), \
                                          self.cf.get("Selenium", "base_url"))
        self.selenium.start()
        self.selenium.window_maximize()
        self.selenium.open('/');

    def tearDown(self):
        """
        This method runs after every 'test' method
        """
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)