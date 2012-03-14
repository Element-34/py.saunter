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

from tailored.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from saunter.testcase.base import BaseTestCase
from saunter.SaunterWebDriver import SaunterWebDriver
from _pytest.mark import MarkInfo

capabilities_map = {
    "firefox": DesiredCapabilities.FIREFOX,
    "iexplore": DesiredCapabilities.INTERNETEXPLORER,
    "chrome": DesiredCapabilities.CHROME
}

os_map = {
    "Windows 2003": "XP",
    "Windows 2008": "VISTA",
    "Linux": "LINUX"
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
        self.verificationErrors = []
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        if self.cf.getboolean("SauceLabs", "ondemand"):
            desired_capabilities = {
                "platform": self.cf.get("SauceLabs", "os"),
                "browserName": self.cf.get("SauceLabs", "browser"),
                "version": self.cf.get("SauceLabs", "browser_version"),
                "name": self._testMethodName
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
            command_executor = "http://%s:%s/wd/hub" % (self.cf.get("Selenium", "server_host"), self.cf.get("Selenium", "server_port"))
        self.driver = WebDriver(desired_capabilities = desired_capabilities, command_executor = command_executor)

        if self.cf.getboolean("Saunter", "use_implicit_wait"):
            self.driver.implicitly_wait(self.cf.getint("Saunter", "implicit_wait"))
        
        if self.cf.getboolean("SauceLabs", "ondemand"):
            self.sauce_session = self.driver.session_id
            
    def teardown_method(self, method):
        """
        Default teardown method for all scripts. If run through Sauce Labs OnDemand, the job name, status and tags
        are updated. Also the video and server log are downloaded if so configured.
        """
        
        if hasattr(self, "driver"):
            self.driver.quit()

        if hasattr(self, "cf") and self.cf.getboolean("SauceLabs", "ondemand"):
            # session couldn't be established for some reason
            if not hasattr(self, "sauce_session"):
               return
            sauce_session = self.sauce_session

            j = {}

            # name
            j["name"] = self._testMethodName

            # result
            if self._resultForDoCleanups._excinfo == None and not self.verificationErrors:
                # print("pass")
                j["passed"] = True
            else:
                # print("fail")
                j["passed"] = False

            # tags
            j["tags"] = []
            for keyword in self._resultForDoCleanups.keywords:
                if isinstance(self._resultForDoCleanups.keywords[keyword], MarkInfo):
                    j["tags"].append(keyword)

            # update
            which_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (self.cf.get("SauceLabs", "username"), sauce_session)
            r = requests.put(which_url,
                             data=json.dumps(j),
                             headers={"Content-Type": "application/json"},
                             auth=(self.cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key")))
            r.raise_for_status()

            if self.cf.getboolean("SauceLabs", "get_video"):
                self.fetch_sauce_artifact("video.flv")

            if self.cf.getboolean("SauceLabs", "get_log"):
                self.fetch_sauce_artifact("selenium-server.log")
                
    # def fetch_artifact(session, which):
    #     which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (self.cf.get("SauceLabs", "username"), session, which)
    #     code = 404
    #     timeout = 0
    #     while code in [401, 404]:
    #         r = requests.get(which_url, auth = (cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key")))
    #         try:
    #             code = r.status_code
    #             r.raise_for_status()
    #         except urllib2.HTTPError, e:
    #             time.sleep(4)
    # 
    #     artifact = open(os.path.join(os.path.dirname(__file__), "logs", which), "wb")
    #     artifact.write(r.content)