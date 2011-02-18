import unittest2 as unittest

import logging

from SeleniumWrapper import SeleniumWrapper as wrapper

import ConfigWrapper

if ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
    import json

class CustomTestCase(unittest.TestCase):
    def setUp(self):
        self.verificationErrors = []
        self.cf = ConfigWrapper.ConfigWrapper().config
        if self.cf.getboolean("SauceLabs", "ondemand"):
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
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            self.sauce_session = self.selenium.get_eval("selenium.sessionId")
        
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

        if self.cf.getboolean("SauceLabs", "ondemand"):
            if self.cf.getboolean("SauceLabs", "get_video") or self.cf.getboolean("SauceLabs", "get_log"):
                def fetch_artifact(which):
                    import os.path
                    import time
                    import urllib2

                    auth_handler = urllib2.HTTPBasicAuthHandler()
                    auth_handler.add_password("Sauce", "https://saucelabs.com/", self.cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key"))
                    opener = urllib2.build_opener(auth_handler)
                    urllib2.install_opener(opener)

                    which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (self.cf.get("SauceLabs", "username"), self.sauce_session, which)
                    code = 404
                    while code == 404:
                        req = urllib2.Request(which_url)
                        try:
                            response = urllib2.urlopen(req)
                            # implicit
                            code = 200
                        except urllib2.URLError, e:
                            if e.code == 404:
                                code = e.code
                                time.sleep(2)
                            if e.code == 401:
                                print("401'ing -- this shouldn't be happening...")
                                break

                    artifact = open(os.path.join(os.path.dirname(__file__), "..", "logs", which), "wb")
                    artifact.write(response.read())
                    
                if self.cf.getboolean("SauceLabs", "get_video"):
                    fetch_artifact("video.flv")
                
                if self.cf.getboolean("SauceLabs", "get_log"):
                    fetch_artifact("selenium-server.log")
        
        self.assertEqual([], self.verificationErrors)

    def verifyEqual(self, want, got):
        try:
            self.assertEqual(want, got)
        except AssertionError, e:
            self.verificationErrors.append(str(e))