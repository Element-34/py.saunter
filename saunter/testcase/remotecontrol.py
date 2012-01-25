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
SaunterTestCase
===============
"""
import ConfigParser
import logging
import os

from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

import saunter.ConfigWrapper
try:
    if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
        import json
except ConfigParser.NoSectionError as e:
    if "DOCGENERATION" not in os.environ:
        raise

from saunter.testcase.base import BaseTestCase

class SaunterTestCase(BaseTestCase):
    """
    Parent class of all script classes used for custom asserts (usually 'soft' asserts) and shared fixture setup
    and teardown
    """
    def setUp(self):
        """
        Default setup method for all scripts. Connects either to the RC server configured in conf/selenium.ini
        or to Sauce Labs OnDemand
        """
        self.verificationErrors = []
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        self.cf.set("Saunter", "name", self._testMethodName)
        if self.cf.getboolean("SauceLabs", "ondemand"):
            host = self.cf.get("SauceLabs", "server_host")
            port = self.cf.get("SauceLabs", "server_port")
            j = {}
            j['username'] = self.cf.get("SauceLabs", "username")
            j['access-key'] = self.cf.get("SauceLabs", "key")
            j['os'] = self.cf.get("SauceLabs", "os")
            j['browser'] = self.cf.get("SauceLabs", "browser")
            if j['browser'][0] == "*":
                j['browser'] = j['browser'][1:]
            j['browser-version'] = self.cf.get("SauceLabs", "browser_version")
            browser = json.dumps(j)
        else:
            host = self.cf.get("Selenium", "server_host")
            port = self.cf.get("Selenium", "server_port")
            browser = self.cf.get("Selenium", "browser")

        self.selenium = wrapper().remote_control(host, port, browser, self.cf.get("Selenium", "base_url"))
        self.selenium.start()
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            wrapper().sauce_session = self.selenium.get_eval("selenium.sessionId")
        
        self.selenium.window_maximize()
        if self.cf.has_option("Selenium", "timeout"):
            self.selenium.set_timeout(self.cf.getint("Selenium", "timeout") * 1000)
        self.selenium.open(self.cf.get("Selenium", "base_url"));

    def tearDown(self):
        """
        Default teardown method for all scripts. If run through Sauce Labs OnDemand, the job name, status and tags
        are updated. Also the video and server log are downloaded if so configured.
        """
        if not self.cf.getboolean("SauceLabs", "ondemand"):
            self.selenium.take_named_screenshot("final")
        self.selenium.stop()
        self.assertEqual([], self.verificationErrors)