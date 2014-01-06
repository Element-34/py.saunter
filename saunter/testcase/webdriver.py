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

try:
    from tailored.webdriver import WebDriver
except ImportError as e:
    if "DOCGENERATION" not in os.environ:
        raise

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

from saunter.matchers import Matchers

capabilities_map = {
    "firefox": DesiredCapabilities.FIREFOX,
    "internet explorer": DesiredCapabilities.INTERNETEXPLORER,
    "internetexplorer": DesiredCapabilities.INTERNETEXPLORER,
    "iexplore": DesiredCapabilities.INTERNETEXPLORER,
    "ie": DesiredCapabilities.INTERNETEXPLORER,
    "chrome": DesiredCapabilities.CHROME,
    "opera": DesiredCapabilities.OPERA,
    "chrome": DesiredCapabilities.CHROME,
    "htmlunitjs": DesiredCapabilities.HTMLUNITWITHJS,
    "htmlunit": DesiredCapabilities.HTMLUNIT,
    "iphone": DesiredCapabilities.IPHONE,
    "ipad": DesiredCapabilities.IPAD,
    "android": DesiredCapabilities.ANDROID,
    "phantomjs": DesiredCapabilities.PHANTOMJS,
}

os_map = {
    "XP": "XP",
    "Windows 2003": "XP",
    "VISTA": "VISTA",
    "Windows 2008": "VISTA",
    "Linux": "LINUX",
    "LINUX": "LINUX",
    "MAC": "MAC"
}


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

        browser = self.cf["browsers"][self.cf["saunter"]["default_browser"]]
        if browser["type"][0] == "*":
            browser = browser["type"] = browser["type"][1:]

        profile = None
        if browser["type"] == 'firefox':
            if browser["profiles"][sys.platform]:
                profile_path = os.path.join(self.cf["saunter"]["base"], 'support', 'profiles', browser["profiles"][sys.platform])
            elif browser["profiles"]["profile"]:
                profile_path = os.path.join(self.cf["saunter"]["base"], 'support', 'profiles', browser["profiles"]["profile"])
            else:
                profile_path = None

            if profile_path:
                if os.path.isdir(profile_path):
                    profile = FirefoxProfile(profile_path)
                else:
                    raise ProfileNotFound("Profile not found at %s" % profile_path)

        if browser["sauce labs"]["ondemand"]:
            desired_capabilities = {
                "platform": browser["sauce labs"]["os"],
                "browserName": browser["type"],
                "version": browser["sauce labs"]["version"],
                "name": method.__name__
            }
            if desired_capabilities["platform"] in os_map:
                desired_capabilities["platform"] = os_map[desired_capabilities["platform"]]

            if browser['sauce labs']['selenium version']:
                desired_capabilities['selenium-version'] = browser['sauce labs']['selenium version']

            if "disable" in self.cf["sauce labs"]:
                if "record video" in self.cf["sauce labs"]["disable"]:
                    if self.cf["sauce labs"]["disable"]["record video"] == True:
                        desired_capabilities['record-video'] = False
                if "upload video on pass" in self.cf["sauce labs"]["disable"]:
                    if self.cf["sauce labs"]["disable"]["upload video on pass"] == True:
                        desired_capabilities['video-upload-on-pass'] = False
                if "step screenshots" in self.cf["sauce labs"]["disable"]:
                    if self.cf["sauce labs"]["disable"]["step screenshots"] == True:
                        desired_capabilities['record-screenshots'] = False
                if "sauce advisor" in self.cf["sauce labs"]["disable"]:
                    if self.cf["sauce labs"]["disable"]["sauce advisor"] == True:
                        desired_capabilities['sauce-advisor'] = False

            if "enable" in self.cf["sauce labs"]:
                if "source capture" in self.cf["sauce labs"]["enable"]:
                    if self.cf["sauce labs"]["enable"]["source capture"] == True:
                        desired_capabilities['source capture'] = True
                if "error screenshots" in self.cf["sauce labs"]["enable"]:
                    if self.cf["sauce labs"]["enable"]["error screenshots"] == True:
                        desired_capabilities['webdriver.remote.quietExceptions'] = True

            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (self.cf["sauce labs"]["username"], self.cf["sauce labs"]["key"])
        else:
            desired_capabilities = capabilities_map[browser["type"]]

            if browser["proxy"]["type"] and browser["proxy"]["type"].lower() == "browsermob":
                from browsermobproxy import Client
                self.client = Client(self.cf.get("Proxy", "proxy_url"))
                self.client.add_to_webdriver_capabilities(desired_capabilities)

            if "is grid" in self.cf["selenium"] and self.cf["selenium"]["executor"]["is grid"]:
                    if browser["grid filters"]["platform"]:
                        desired_capabilities["platform"] = browser["grid filters"]["platform"].upper()
                    if browser["grid filters"]["version"]:
                        desired_capabilities["platform"] = str(browser["grid filters"]["version"])

            command_executor = "http://%s:%s/wd/hub" % (self.cf["selenium"]["executor"]["host"], self.cf["selenium"]["executor"]["port"])

        # print(desired_capabilities)
        self.driver = WebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor, browser_profile=profile)

        self.verificationErrors = []
        self.matchers = Matchers(self.driver, self.verificationErrors)

        if browser["sauce labs"]["ondemand"]:
            self.sauce_session = self.driver.session_id

        self._screenshot_number = 1

    def teardown_method(self, method):
        """
        Default teardown method for all scripts. If run through Sauce Labs OnDemand, the job name, status and tags
        are updated. Also the video and server log are downloaded if so configured.
        """
        if hasattr(self, "config"):
            if "sauce labs" in self.cf["browsers"][self.cf["saunter"]["default_browser"]] and not self.cf["browsers"][self.cf["saunter"]["default_browser"]]["sauce labs"]["ondemand"]:
                self.take_named_screenshot("final")

        if hasattr(self, "driver"):
            self.driver.quit()

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
