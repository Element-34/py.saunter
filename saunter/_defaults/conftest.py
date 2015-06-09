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

import os
import os.path
import py
import sys
import random
import saunter.saucelabs
import saunter.ConfigWrapper

def pytest_configure(config):
    cwd = os.getcwd()
    sys.path.append(os.path.join(cwd, "modules"))
    saunter_config = saunter.ConfigWrapper.ConfigWrapper()
    saunter_config["saunter"] = {}
    saunter_config["saunter"]["base"] = cwd
    saunter_config["saunter"]["log_dir"] = os.environ["SAUNTER_LOG_DIR"]
    saunter_config.configure()

    # create the proxy instances we'll need; one per instance
    saunter_config['saunter']['proxies'] = []
    if saunter_config['selenium']['proxy']['url'] != '' and saunter_config['selenium']['proxy']['type'].lower() == 'browsermob':
        from browsermobproxy import Client
        for x in range(0, int(os.environ["SAUNTER_PARALLEL"])):
            saunter_config['saunter']['proxies'].append(Client(saunter_config['selenium']['proxy']['url']))

def pytest_unconfigure(config):
    saunter_config = saunter.ConfigWrapper.ConfigWrapper()
    for proxy in saunter_config['saunter']['proxies']:
        proxy.close()

# Comment or remove to disable auto screenshotting on error
def pytest_runtest_call(item, __multicall__):
    try:
        __multicall__.execute()
    except Exception as e:
        if hasattr(item.parent.obj, 'driver') or hasattr(item.parent.obj, 'selenium'):
            item.parent.obj.take_named_screenshot('exception')
        raise

def pytest_runtest_makereport(__multicall__, item, call):
    if call.when == "call":
        try:
            if len(item.parent.obj.verificationErrors) != 0:
                if call.excinfo:
                    bits = call.excinfo.exconly().split(':')
                    raise AssertionError({bits[0]: call.excinfo.exconly()[len(bits[0]) + 2:], "Verification Failures": item.parent.obj.verificationErrors})
                else:
                    raise AssertionError(item.parent.obj.verificationErrors)
        except AssertionError:
            call.excinfo = py.code.ExceptionInfo()

    report = __multicall__.execute()

    item.outcome = report.outcome

    if call.when == "call":
        if hasattr(item.parent.obj, 'config') and item.parent.obj.config["browsers"][item.parent.obj.config["saunter"]["default_browser"]]["sauce labs"]["ondemand"]:
            s = saunter.saucelabs.SauceLabs(item.parent.obj.config["sauce labs"]["username"], item.parent.obj.config["sauce labs"]["key"])
            s.update_job_from_item(item)

    return report

def pytest_runtest_teardown(__multicall__, item):
    __multicall__.execute()

    if hasattr(item.parent.obj, 'config') and item.parent.obj.config["browsers"][item.parent.obj.config["saunter"]["default_browser"]]["sauce labs"]["ondemand"]:
        s = saunter.saucelabs.SauceLabs(item.parent.obj.config["sauce labs"]["username"], item.parent.obj.config["sauce labs"]["key"])
        s.update_job_from_item(item)

def pytest_collection_modifyitems(items):
    random.shuffle(items)