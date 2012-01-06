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

import saunter.ConfigWrapper

if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
    import json

cf = saunter.ConfigWrapper.ConfigWrapper().config

import os.path
import time
import requests
import urllib2

import py
import _pytest

from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

def fetch_artifact(which):
    sauce_session = wrapper().sauce_session
    which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (cf.get("SauceLabs", "username"), sauce_session, which)
    code = 404
    timeout = 0
    while code in [401, 404]:
        r = requests.get(which_url, auth = (cf.get("SauceLabs", "username"), cf.get("SauceLabs", "key")))
        try:
            code = r.status_code
            r.raise_for_status()
        except urllib2.HTTPError, e:
            time.sleep(4)

    artifact = open(os.path.join(os.path.dirname(__file__), "logs", which), "wb")
    artifact.write(r.content)

def pytest_runtest_logreport(report):
    # this will make sure the browser is dead even if there was an exception in setUp
    try:
        c = wrapper().connection
        if c.running:
            if hasattr(c, "capabilities"):
                c.quit()
            else:
                c.stop()
    except AttributeError:
        pass
        
    if cf.getboolean("SauceLabs", "ondemand"):
        # session couldn't be established for some reason
        if not hasattr(wrapper(), "sauce_session"):
           return
        sauce_session = wrapper().sauce_session
        
        j = {}
    
        # name
        names = report.nodeid.split("::")
        names[0] = names[0].replace("/", '.')
        names = tuple(names)
        d = {}
        names = [x.replace(".py", "") for x in names if x != "()"]
        classnames = names[:-1]
        d['classname'] = ".".join(classnames)
        d['name'] = py.xml.escape(names[-1])
        attrs = ['%s="%s"' % item for item in sorted(d.items())]
        j["name"] = d['name']
    
        # result
        if report.passed:
            j["passed"] = True
        else:
            j["passed"] = False

        # tags
        j["tags"] = report.keywords
        
        # update
        which_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (cf.get("SauceLabs", "username"), sauce_session)
        r = requests.put(which_url,
                         data=json.dumps(j),
                         headers={"Content-Type": "application/json"},
                         auth=(cf.get("SauceLabs", "username"), cf.get("SauceLabs", "key")))
        r.raise_for_status()

        if cf.getboolean("SauceLabs", "get_video"):
            fetch_artifact("video.flv")
        
        if cf.getboolean("SauceLabs", "get_log"):
            fetch_artifact("selenium-server.log")