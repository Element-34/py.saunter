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

import unittest2 as unittest
import requests
import time
import urllib2
import os
import os.path
from _pytest.mark import MarkInfo
import json

class BaseTestCase(unittest.TestCase):
    def _saucelabs(self, method):
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
        
    
    def fetch_sauce_artifact(self, which):
        sauce_session = self.sauce_session
        which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (self.cf.get("SauceLabs", "username"), sauce_session, which)
        code = 404
        timeout = 0
        while code in [401, 404]:
            r = requests.get(which_url, auth = (self.cf.get("SauceLabs", "username"), self.cf.get("SauceLabs", "key")))
            try:
                code = r.status_code
                r.raise_for_status()
            except requests.exceptions.HTTPError, e:
                time.sleep(4)

        artifact = open(os.path.join(self.cf.get("Saunter", "base"), "logs", which), "wb")
        artifact.write(r.content)
        artifact.close()
    
    def verify_equal(self, want, got, message = ""):
        try:
            self.assertEqual(want, got)
        except AssertionError, e:
            if message:
                m = "%s:\n%s" % (message, str(e))
            else:
                m = str(e)
            self.verificationErrors.append(m)

    def verify_text_present(self, text, message = ""):
        try:
            self.assertTrue(self.selenium.is_text_present(text))
        except AssertionError, e:
            if message:
                m = "%s:\n%s" % (message, str(e))
            else:
                m = str(e)
            self.verificationErrors.append(m)

    def verify_element_present(self, locator, message = ""):
        try:
            self.assertTrue(self.selenium.is_element_present(locator))
        except AssertionError, e:
            if message:
                m = "%s:\n%s" % (message, str(e))
            else:
                m = str(e)
            self.verificationErrors.append(m)

    def verify_visible(self, locator, message = ""):
        try:
            self.assertTrue(self.selenium.is_visible(locator))
        except AssertionError, e:
            if message:
                m = "%s:\n%s" % (message, str(e))
            else:
                m = str(e)
            self.verificationErrors.append(m)

    def verify_true(self, condition, message = ""):
        try:
            self.assertTrue(condition)
        except AssertionError, e:
            if message:
                m = "%s:\n%s" % (message, str(e))
            else:
                m = str(e)
            self.verificationErrors.append(m)
