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


import zipfile
try:
    from io import BytesIO
except ImportError:
    from cStringIO import StringIO as BytesIO
    bytes = str
    str = unicode

from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

import saunter.ConfigWrapper
from saunter.matchers import Matchers
from saunter.exceptions import ProfileNotFound

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
    def setup_method(self, method):
        """
        Default setup method for all scripts. Connects either to the RC server configured in conf/selenium.ini
        or to Sauce Labs OnDemand
        """
        self.config = saunter.ConfigWrapper.ConfigWrapper().config
        self.cf = self.config

        self.current_method_name = method.__name__

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

            if j['browser'] == "firefox":
                if self.cf.has_option("Selenium", "profile-%s" % sys.platform):
                    profile_path = os.path.join(self.cf.get("Saunter", "base"), 'support', 'profiles', self.cf.get("Selenium", "profile-%s" % sys.platform))
                elif self.cf.has_option("Selenium", "profile"):
                    profile_path = os.path.join(self.cf.get("Saunter", "base"), 'support', 'profiles', self.cf.get("Selenium", "profile"))

                if os.path.isdir(profile_path):
                    profile_zip = os.path.join(self.cf.get("Saunter", "base"), 'support', 'profiles', "%s.zip" % self.cf.get("Selenium", "profile"))
                    
                    zipped = zipfile.ZipFile(profile_zip, 'w', zipfile.ZIP_DEFLATED)
                    path_root = len(profile_path) + 1 # account for trailing slash
                    for base, dirs, files in os.walk(profile_path):
                        for fyle in files:
                            filename = os.path.join(base, fyle)
                            zipped.write(filename, filename[path_root:])
                    zipped.close()
                else:
                    raise ProfileNotFound("Profile not found at %s" % profile_path)
                j['firefox-profile-url'] = "%s/profiles/%s.zip" % (self.cf.get("YourCompany", "file_server_base"), self.cf.get("Selenium", "profile"))
            j['browser-version'] = self.cf.get("SauceLabs", "browser_version")

            if self.cf.has_option("SauceLabs", "selenium_version"):
                j['selenium-version'] = self.cf.get('SauceLabs', 'selenium_version')

            browser = json.dumps(j)
            # print(browser)
        else:
            host = self.cf.get("Selenium", "server_host")
            port = self.cf.get("Selenium", "server_port")
            browser = self.cf.get("Selenium", "browser")

        self.selenium = wrapper().remote_control(host, port, browser, self.cf.get("Selenium", "base_url"))
        self.selenium.start()

        self.verificationErrors = []
        self.matchers = Matchers(self.selenium, self.verificationErrors)
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            self.sauce_session = self.selenium.get_eval("selenium.sessionId")
            
        
        self.selenium.window_maximize()
        if self.cf.has_option("Selenium", "timeout"):
            self.selenium.set_timeout(self.cf.getint("Selenium", "timeout") * 1000)
        self.selenium.open(self.cf.get("Selenium", "base_url"));

        self._screenshot_number = 1

    def teardown_method(self, method):
        if hasattr(self, "cf") and not self.cf.getboolean("SauceLabs", "ondemand"):
            self.take_named_screenshot("final")
        
        self.selenium.stop()

    def take_numbered_screenshot(self):
        if self.config.has_option("Saunter", "take_screenshots"):
            if self.cf.getboolean("Saunter", "take_screenshots"):
                method_dir = self._screenshot_prep_dirs()

                self.selenium.capture_screenshot(os.path.join(method_dir, str(self._screenshot_number).zfill(3) + ".png"))
                self._screenshot_number = self._screenshot_number + 1

                if self.config.has_option("Saunter", "jenkins"):
                    if self.cf.getboolean("Saunter", "jenkins"):
                        sys.stdout.write(os.linesep + "[[ATTACHMENT|%s]]" % image_path + os.linesep)

    def take_named_screenshot(self, name):
        method_dir = self._screenshot_prep_dirs()

        self.selenium.capture_screenshot(os.path.join(method_dir, str(name) + ".png"))

        if self.config.has_option("Saunter", "jenkins"):
            if self.cf.getboolean("Saunter", "jenkins"):
                sys.stdout.write(os.linesep + "[[ATTACHMENT|%s]]" % image_path + os.linesep)
