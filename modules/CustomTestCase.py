import unittest2 as unittest

import logging

from SeleniumWrapper import SeleniumWrapper as wrapper

import ConfigWrapper

class CustomTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.cf = ConfigWrapper.ConfigWrapper().config
        if self.cf.getboolean("SauceLabs", "ondemand"):
            import json
            
            host = self.cf.get("SauceLabs", "server_host")
            port = self.cf.get("SauceLabs", "server_port")
            j = {}
            j['username'] = self.cf.get("SauceLabs", "username")
            j['access-key'] = self.cf.get("SauceLabs", "key")
            j['os'] = self.cf.get("SauceLabs", "os")
            j['browser'] = self.cf.get("SauceLabs", "browser")
            j['browser-version'] = self.cf.get("SauceLabs", "browser_version")
            browser = json.dumps(j)
        else:
            host = self.cf.get("Selenium", "server_host")
            port = self.cf.get("Selenium", "server_port")
            browser = self.cf.get("Selenium", "browser")

        self.selenium = wrapper().connect(host, port, browser, self.cf.get("Selenium", "base_url"))
        self.selenium.start()
        self.selenium.window_maximize()
        self.selenium.open('/');

    def tearDown(self):
        """
        This method runs after every 'test' method
        """
        if self.cf.getboolean("SauceLabs", "ondemand"):
            j = {}

            # name
            j["name"] = self._testMethodName

            # result
            if (len(self._resultForDoCleanups.result.failures) != 0) or \
               (len(self._resultForDoCleanups.result.errors) != 0) or \
               (len(self.verificationErrors) != 0):
                j["passed"] = False
            else:
                j["passed"] = True

            # tags
            j["tags"] = getattr(getattr(self, self._testMethodName), 'tags')
            self.selenium.set_context('sauce: job-info=%s' % json.dumps(j))
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)

    def verifyEqual(self, want, got):
        try:
            self.assertEqual(want, got)
        except AssertionError, e:
            self.verificationErrors.append(str(e))