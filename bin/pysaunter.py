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
import markfiltration
import argparse
import os
import os.path
import re
import shutil
import sys
import time
import tempfile
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
    
    # scripts
    if not os.path.isdir(os.path.join(cwd, "scripts")):
        os.mkdir(os.path.join(cwd, "scripts"))

    # support
    if not os.path.isdir(os.path.join(cwd, "support")):
        os.mkdir(os.path.join(cwd, "support"))

    # support/csv
    if not os.path.isdir(os.path.join(cwd, "support", "csv")):
        os.mkdir(os.path.join(cwd, "support", "csv"))
        
    # misc.
    if not os.path.isfile(os.path.join(cwd, "conftest.py")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "conftest.py"), cwd)
    if not os.path.isfile(os.path.join(cwd, "pytest.ini")):
        shutil.copy(os.path.join(saunter_installed_at, "_defaults", "pytest.ini"), cwd)

    sys.exit()

p = argparse.ArgumentParser()
p.add_argument('--new', action='store_true', default=False)
p.add_argument('-f', action='store', default='shallow', nargs='*')
p.add_argument('-v', action='store_true', default=None)
p.add_argument('-s', action='store_true', default=None)

results = p.parse_args()

# pythonpath
sys.path.append(os.path.join(cwd, "modules"))

import saunter.SeleniumServer

# check if server is up
if not saunter.SeleniumServer.have_server():
    if 'HUDSON_HOME' in os.environ or 'JENKINS_HOME' in os.environ:
      sys.exit("The Selenium Server must be started outside of the Hudson/Jenkins Agent")
    saunter.SeleniumServer.start_server()

arguments = sys.argv[1:]
if '--new' in arguments:
    new()

# logging
log_name = os.path.join(cws, 'logs', "%s.xml" % time.strftime("%Y-%m-%d-%M-%S"))
arguments.append('--junitxml=%s' %log_name)
arguments.append('--tb=line')

# run
arguments.append("scripts")
pytest.main(args=arguments, plugins=[marks.MarksDecorator(), markfiltration.MarkFiltration()])

shutil.copy(log_name, os.path.join(cwd, 'logs', 'latest.xml'))

if os.path.exists(os.path.join(tempfile.gettempdir(), "selenium-server.pid")):
  saunter.SeleniumServer.stop_server()