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

import requests
import time
import urllib2
import os
import os.path
from _pytest.mark import MarkInfo
import json
import saunter.matchers as matchers

class BaseTestCase(object):
    def _saucelabs(self, method):
        # session couldn't be established for some reason
        if not hasattr(self, "sauce_session"):
           return
        sauce_session = self.sauce_session

        j = {}

        # name
        j["name"] = method.__name__

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

    def assertEqual(self, first, second, msg=None):
        self.matchers.assert_equal(first, second, msg)

    def assertNotEqual(self, first, second, msg=None):
        self.matchers.assert_not_equal(first, second, msg)

    def assertTrue(self, expr, msg=None):
        self.matchers.assert_true(expr, msg)

    def assertFalse(self, expr, msg=None):
        self.matchers.assert_false(expr, msg)

    def assertIs(self, first, second, msg=None):
        self.matchers.assert_is(first, second, msg)

    def assertIsNot(self, first, second, msg=None):
        self.matchers.assert_is_not(first, second, msg)

    def assertIsNone(self, expr, msg=None):
        self.matchers.assert_is_none(expr, msg)

    def assertIsNotNone(self, expr, msg=None):
        self.matchers.assert_is_not_none(expr, msg)

    def assertIn(self, first, second, msg=None):
        self.matchers.assert_in(first, second, msg)

    def assertNotIn(self, first, second, msg=None):
        self.matchers.assert_not_in(first, second, msg)

    def assertIsInstance(self, obj, cls, msg=None):
        self.matchers.assert_is_instance(obj, cls, msg)

    def assertIsNotInstance(self, obj, cls, msg=None):
        self.matchers.assert_is_not_instance(obj, cls, msg)
    
    
        
        
        
        