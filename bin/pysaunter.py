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

import datetime
import pytest
import marks
import argparse
import os
import os.path
import re
import shutil
import sys
import time
import tempfile
import types
import saunter
saunter_installed_at = os.path.dirname(saunter.__file__)
cwd = os.getcwd()

def new():
    # conf
    if not os.path.isdir(os.path.join(cwd, "conf")):
        os.mkdir(os.path.join(cwd, "conf"))
    if not os.path.isfile(os.path.join(cwd, "conf", "saunter.ini.default")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "conf", "saunter.ini.default"),
                    os.path.join(cwd, "conf"))
        
    # log
    if not os.path.isdir(os.path.join(cwd, "logs")):
        os.mkdir(os.path.join(cwd, "logs"))

    # modules
    if not os.path.isdir(os.path.join(cwd, "modules")):
        os.mkdir(os.path.join(cwd, "modules"))

    # modules/pages
    if not os.path.isdir(os.path.join(cwd, "modules", "pages")):
        os.mkdir(os.path.join(cwd, "modules", "pages"))

    # pages is a package
    if not os.path.isfile(os.path.join(cwd, "modules", "pages", "__init__.py")):
        f = open(os.path.join(cwd, "modules", "pages", "__init__.py"), "w")
        f.close()

    # modules/providers
    if not os.path.isdir(os.path.join(cwd, "modules", "providers")):
        os.mkdir(os.path.join(cwd, "modules", "providers"))

    # providers is a package
    if not os.path.isfile(os.path.join(cwd, "modules", "providers", "__init__.py")):
        f = open(os.path.join(cwd, "modules", "providers", "__init__.py"), "w")
        f.close()

    # modules/pages
    if not os.path.isdir(os.path.join(cwd, "modules", "tailored")):
        os.mkdir(os.path.join(cwd, "modules", "tailored"))

    # pages is a package
    if not os.path.isfile(os.path.join(cwd, "modules", "tailored", "__init__.py")):
        f = open(os.path.join(cwd, "modules", "tailored", "__init__.py"), "w")
        f.close()
        
    if not os.path.isfile(os.path.join(cwd, "modules", "tailored", "remotecontrol.py")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "tailored", "remotecontrol.py"), os.path.join(cwd, "modules", "tailored"))

    # scripts
    if not os.path.isdir(os.path.join(cwd, "scripts")):
        os.mkdir(os.path.join(cwd, "scripts"))

    # support
    if not os.path.isdir(os.path.join(cwd, "support")):
        os.mkdir(os.path.join(cwd, "support"))

    # support/csv
    if not os.path.isdir(os.path.join(cwd, "support", "csv")):
        os.mkdir(os.path.join(cwd, "support", "csv"))

    # support/db
    if not os.path.isdir(os.path.join(cwd, "support", "db")):
        os.mkdir(os.path.join(cwd, "support", "db"))
        
    # misc.
    if not os.path.isfile(os.path.join(cwd, "conftest.py")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "conftest.py"), cwd)
    if not os.path.isfile(os.path.join(cwd, "pytest.ini")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "pytest.ini"), cwd)

    sys.exit()

p = argparse.ArgumentParser()
p.add_argument('--new', action='store_true', default=False, help="creates a new Py.Saunter environment")
p.add_argument('-v', action='store_true', default=None, help="increase verbosity")
p.add_argument('-s', action='store_true', default=None, help="don't capture output")
p.add_argument('--tb', action='store', default="native", help='traceback print mode (long/short/line/native/no)')
p.add_argument('-p', action='append', default=[], help="early-load given plugin (multi-allowed)")
p.add_argument('-m', action='append', default=[], help="filter based on marks")
p.add_argument('--traceconfig', action='store_true', default=None, help="trace considerations of conftest.py files")
p.add_argument('--pdb', action='store_true', default=None, help="start the interactive Python debugger on errors")
p.add_argument('--maxfail', action='store', default=None, help="exit after first num failures or errors.")
p.add_argument('--collectonly', action='store_true', default=None, help="only collect tests, don't execute them")
p.add_argument('--durations', action='store', default=None, help='show N slowest setup/test durations (N=0 for all)')

results = p.parse_args()

# argument handling; what a mess
if results.new:
    new()

arguments = []

# argparse will take all the -m arguments and compile them into a list
if len(results.m) == 1:
    arguments.append("-m")
    arguments.append(results.m[0])
elif len(results.m) > 1:
    for markers in results.m:
        arguments.append("-m")
        arguments.append(markers)
else:
    arguments.append("-m")
    arguments.append("shallow")

# this are either true or false
for noneable in ['v', 's']:
    if noneable in results.__dict__ and results.__dict__[noneable] != None:
        arguments.append("-%s" % noneable)

for noneable in ['traceconfig', 'pdb', 'collectonly']:
    if noneable in results.__dict__ and results.__dict__[noneable] != None:
        arguments.append("--%s" % noneable)

for has_value in ['maxfail', 'durations']:
    if has_value in results.__dict__ and results.__dict__[has_value] != None:
        arguments.append("--%s=%s" % (has_value, results.__dict__[has_value][0]))
        # arguments.append(results.__dict__[has_value][0])        

# plugin control
if len(results.p) == 1:
    arguments.append("-p")
    arguments.append(results.p[0])
else:
    for p in results.p:
        arguments.append("-p")
        arguments.append(p)

# pythonpath
sys.path.append(os.path.join(cwd, "modules"))

import saunter.SeleniumServer

import saunter.ConfigWrapper
saunter.ConfigWrapper.ConfigWrapper().config.set("Saunter", "base", cwd)

# check if server is up
if not saunter.SeleniumServer.have_server():
    if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("Selenium", "manage_server"):
        if 'HUDSON_HOME' in os.environ or 'JENKINS_HOME' in os.environ:
          sys.exit("The Selenium Server must be started outside of the Hudson/Jenkins Agent")
        started = saunter.SeleniumServer.start_server()
        if not started:
            sys.exit("Could not start the Selenium Server")
    else:
        sys.exit("Selenium Server not running and py.saunter configured not to control it")

# logging
log_name = os.path.join(cwd, 'logs', "%s.xml" % time.strftime("%Y-%m-%d-%H-%M-%S"))
arguments.append('--junitxml=%s' %log_name)

arguments.append('--tb=%s' % results.__dict__["tb"])

# run
arguments.append("scripts")

run_status = pytest.main(args=arguments, plugins=[marks.MarksDecorator()])

shutil.copy(log_name, os.path.join(cwd, 'logs', 'latest.xml'))

if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("Selenium", "manage_server"):
    if os.path.exists(os.path.join(tempfile.gettempdir(), "selenium-server.pid")):
        try:
            saunter.SeleniumServer.stop_server()
        except OSError as (errno, strerror):
            if strerror == "No such process":
                print("Tried to kill Selenium Server but process in was already killed.")
                run_status = 1

sys.exit(run_status)