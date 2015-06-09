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
import json
import logging
import os
import os.path
import requests
import sys

import saunter.ConfigWrapper


import saunter.browser
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from saunter.exceptions import ProfileNotFound
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from saunter.testcase.base import BaseTestCase
from selenium.webdriver import FirefoxProfile
import py.test
from _pytest.mark import MarkInfo
import saunter.saucelabs

from saunter.matchers import Matchers

class SaunterTestCase(BaseTestCase):
    """
    Parent class of all script classes used for custom asserts (usually 'soft' asserts) and shared fixture setup
    and teardown
    """
    def setup_method(self, method):
        """
        Parent class of all script classes used for custom asserts (usually 'soft' asserts) and shared fixture setup
        and teardown
        """
        self.cf = self.config = saunter.ConfigWrapper.ConfigWrapper()

        self.current_method_name = method.__name__

        default_browser = self.cf["browsers"][self.cf["saunter"]["default_browser"]]
        self.browser = saunter.browser.Browser(default_browser, self.cf)
        self.driver = self.browser.driver

        if hasattr(self.browser, 'proxy'):
            self.proxy = self.browser.proxy

        if "sauce labs" in self.cf["browsers"][self.cf["saunter"]["default_browser"]] and \
            self.cf["browsers"][self.cf["saunter"]["default_browser"]]["sauce labs"]["ondemand"] and \
            hasattr(self.driver, "session_id"):
            s = saunter.saucelabs.SauceLabs(self.cf["sauce labs"]["username"], self.cf["sauce labs"]["key"])
            s.update_name(self.driver.session_id, self.current_method_name)

        self.verificationErrors = []
        self.matchers = Matchers(self.driver, self.verificationErrors)

        self._screenshot_number = 1

    def teardown_method(self, method):
        """
        Default teardown method for all scripts. If run through Sauce Labs OnDemand, the job name, status and tags
        are updated. Also the video and server log are downloaded if so configured.
        """
        if hasattr(self, "config"):
            if "sauce labs" in self.cf["browsers"][self.cf["saunter"]["default_browser"]] and \
            not self.cf["browsers"][self.cf["saunter"]["default_browser"]]["sauce labs"]["ondemand"] \
            and self.cf["saunter"]["screenshots"]["on_finish"]:
                self.take_named_screenshot("final")

        if hasattr(self, "driver"):
            self.driver.quit()

        if hasattr(self.browser, 'proxy'):
            self.config['saunter']['proxies'].append(self.proxy)

    def take_numbered_screenshot(self):
        if self.config.has_option("Saunter", "take_screenshots"):
            if self.cf.getboolean("Saunter", "take_screenshots"):
                method_dir = self._screenshot_prep_dirs()

                self.driver.get_screenshot_as_file(os.path.join(method_dir, str(self._screenshot_number).zfill(3) + ".png"))
                self._screenshot_number = self._screenshot_number + 1

                if self.config.has_option("Saunter", "jenkins"):
                    if self.cf.getboolean("Saunter", "jenkins"):
                        sys.stdout.write(os.linesep + "[[ATTACHMENT|%s]]" % image_path + os.linesep)

    def take_named_screenshot(self, name):
        method_dir = self._screenshot_prep_dirs()

        image_path = os.path.join(method_dir, str(name) + ".png")
        self.driver.get_screenshot_as_file(image_path)

        if "ci_type" in self.cf and self.cf["ci_type"].lower() == "jenkins":
            sys.stdout.write(os.linesep + "[[ATTACHMENT|%s]]" % image_path + os.linesep)
