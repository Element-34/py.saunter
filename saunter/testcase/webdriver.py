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
import os.path
import requests

import saunter.ConfigWrapper
try:
    if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
        import json
except ConfigParser.NoSectionError as e:
    if "DOCGENERATION" not in os.environ:
        raise

try:
    from tailored.webdriver import WebDriver
except ImportError as e:
    if "DOCGENERATION" not in os.environ:
        raise

from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from saunter.testcase.base import BaseTestCase
from saunter.SaunterWebDriver import SaunterWebDriver
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
    "android": DesiredCapabilities.ANDROID
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
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        self.config = self.cf

        self.current_method_name = method.__name__

        if self.cf.getboolean("SauceLabs", "ondemand"):
            desired_capabilities = {
                "platform": self.cf.get("SauceLabs", "os"),
                "browserName": self.cf.get("SauceLabs", "browser"),
                "version": self.cf.get("SauceLabs", "browser_version"),
                "name": method.__name__
            }
            if desired_capabilities["browserName"][0] == "*":
                desired_capabilities["browserName"] = desired_capabilities["browserName"][1:]
            if desired_capabilities["platform"] in os_map:
                desired_capabilities["platform"] = os_map[desired_capabilities["platform"]]
            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (self.cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key"))
        else:
            browser = self.cf.get("Selenium", "browser")
            if browser[0] == "*":
                browser = browser[1:]
            if browser == "chrome":
                os.environ["webdriver.chrome.driver"] = self.cf.get("Selenium", "chromedriver_path")
            desired_capabilities = capabilities_map[browser]
            if self.cf.has_section("Proxy") \
                and self.cf.has_option("Proxy", "proxy_url") \
                and (self.cf.has_option("Proxy", "browsermob") and self.cf.getboolean("Proxy", "browsermob")):
                from browsermobproxy import Client
                self.client = Client(self.cf.get("Proxy", "proxy_url"))
                self.client.add_to_webdriver_capabilities(desired_capabilities)
            if self.cf.has_section("Grid"):
                if self.cf.getboolean("Grid", "use_grid") and self.cf.get("Grid", "type") == "selenium":
                    if self.cf.has_option("Grid", "platform"):
                        desired_capabilities["platform"] = self.cf.get("Grid", "platform").upper()
                    if self.cf.has_option("Grid", "version"):
                        desired_capabilities["version"] = str(self.cf.get("Grid", "browser_version"))

            command_executor = "http://%s:%s/wd/hub" % (self.cf.get("Selenium", "server_host"), self.cf.get("Selenium", "server_port"))
        self.driver = WebDriver(desired_capabilities = desired_capabilities, command_executor = command_executor)

        self.verificationErrors = []
        self.matchers = Matchers(self.driver, self.verificationErrors)
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            self.sauce_session = self.driver.session_id

        self._screenshot_number = 1
            
    def teardown_method(self, method):
        """
        Default teardown method for all scripts. If run through Sauce Labs OnDemand, the job name, status and tags
        are updated. Also the video and server log are downloaded if so configured.
        """
        if hasattr(self, "config") and not self.config.getboolean("SauceLabs", "ondemand"):
            self.take_named_screenshot("final")

        if hasattr(self, "driver"):
            self.driver.quit()

    def take_numbered_screenshot(self):
        if self.config.has_option("Saunter", "take_screenshots"):
            if self.cf.getboolean("Saunter", "take_screenshots"):
                method_dir = self._screenshot_prep_dirs()

                self.driver.get_screenshot_as_file(os.path.join(method_dir, str(self._screenshot_number).zfill(3) + ".png"))
                self._screenshot_number = self._screenshot_number + 1

    def take_named_screenshot(self, name):
        method_dir = self._screenshot_prep_dirs()

        self.driver.get_screenshot_as_file(os.path.join(method_dir, str(name) + ".png"))
