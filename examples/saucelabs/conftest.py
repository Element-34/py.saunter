import saunter.ConfigWrapper

if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("SauceLabs", "ondemand"):
    import json

cf = saunter.ConfigWrapper.ConfigWrapper().config

import os.path
import time
import urllib2

import py
import _pytest

from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

class AdvancedReport(_pytest.runner.TestReport):
    def __init__(self, nodeid, location, marks, outcome, longrepr, when):
        super(AdvancedReport, self).__init__(nodeid, location, marks, outcome, longrepr, when)
                
    def __repr__(self):
        return "<AdvancedReport %r when=%r outcome=%r>" % (
            self.nodeid, self.when, self.outcome)

def pytest_runtest_makereport(item, call):
    when = call.when
    # get the MarkInfo objects since 'keyword' is essentially useless.
    marks = []
    for keyword in item.keywords:
        if isinstance(item.keywords[keyword], _pytest.mark.MarkInfo):
            marks.append(keyword)

    excinfo = call.excinfo
    if not call.excinfo:
        outcome = "passed"
        longrepr = None
    else:
        excinfo = call.excinfo
        if not isinstance(excinfo, py.code.ExceptionInfo):
            outcome = "failed"
            longrepr = excinfo
        elif excinfo.errisinstance(py.test.skip.Exception):
            outcome = "skipped"
            r = excinfo._getreprcrash()
            longrepr = (str(r.path), r.lineno, r.message)
        else:
            outcome = "failed"
            if call.when == "call":
                longrepr = item.repr_failure(excinfo)
            else: # exception in setup or teardown
                longrepr = item._repr_failure_py(excinfo)
    return AdvancedReport(item.nodeid, item.location, marks, outcome, longrepr, when)

def fetch_artifact(which):
    sauce_session = wrapper().sauce_session
    auth_handler = urllib2.HTTPBasicAuthHandler()
    auth_handler.add_password("Sauce", "https://saucelabs.com/", cf.get("SauceLabs", "username"), cf.get("SauceLabs", "key"))
    opener = urllib2.build_opener(auth_handler)
    urllib2.install_opener(opener)

    which_url = "https://saucelabs.com/rest/%s/jobs/%s/results/%s" % (cf.get("SauceLabs", "username"), sauce_session, which)
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
                time.sleep(8)
            if e.code == 401:
                print("401'ing -- this shouldn't be happening... But if it does, up the sleep amount by a couple seconds. Ugh.")
                break

    artifact = open(os.path.join(os.path.dirname(__file__), "logs", which), "wb")
    artifact.write(response.read())

def pytest_runtest_logreport(report):
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
        auth_handler = urllib2.HTTPBasicAuthHandler()
        auth_handler.add_password("Sauce", "https://saucelabs.com/", cf.get("SauceLabs", "username"), cf.get("SauceLabs", "key"))
        opener = urllib2.build_opener(auth_handler)
        urllib2.install_opener(opener)

        which_url = "https://saucelabs.com/rest/v1/%s/jobs/%s" % (cf.get("SauceLabs", "username"), sauce_session)
        request = urllib2.Request(which_url, data=json.dumps(j))
        request.add_header('Content-Type', 'your/contenttype')
        request.get_method = lambda: 'PUT'
        url = opener.open(request)
                    
        if cf.getboolean("SauceLabs", "get_video"):
            fetch_artifact("video.flv")
        
        if cf.getboolean("SauceLabs", "get_log"):
            fetch_artifact("selenium-server.log")