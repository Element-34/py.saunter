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
import os.path
import re
import shutil
import sys
import time

p = argparse.ArgumentParser()
p.add_argument('-f', action='store', default='shallow', nargs='*')
p.add_argument('-v', action='store_true', default=None)
p.add_argument('-s', action='store_true', default=None)

results = p.parse_args()

base_dir = os.path.dirname(os.path.abspath(__file__))

# pythonpath
sys.path.append(os.path.join(base_dir, "modules"))

import SeleniumServer

# check if server is up
if not SeleniumServer.have_server():
    if 'HUDSON_HOME' in os.environ or 'JENKINS_HOME' in os.environ:
      sys.exit("The Selenium Server must be started outside of the Hudson/Jenkins Agent")
    SeleniumServer.start_server()

arguments = sys.argv[1:]

# logging
#log_name = os.path.join(base_dir, 'logs', "%s.xml" % time.strftime("%Y-%m-%d-%M-%S"))
log_name = os.path.join(base_dir, 'logs', "testresults.xml")
arguments.append('--junitxml=%s' %log_name)
arguments.append('--tb=line')

# run
arguments.append("scripts")
pytest.main(args=arguments, plugins=[marks.MarksDecorator(), markfiltration.MarkFiltration()])

shutil.copy(log_name, os.path.join(base_dir, 'logs', 'latest.xml'))

if os.path.exists(os.path.join(base_dir, "third_party", "selenium", "server", "server.pid")):
  SeleniumServer.stop_server()