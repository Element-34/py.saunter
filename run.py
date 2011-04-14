import datetime
import nose
from nose.config import Config
import argparse
import os.path
import re
import shutil
import sys
import time

# other arguments necessary as needed; they all get passed down to nose
p = argparse.ArgumentParser()
p.add_argument('-a', action='store', default='shallow')
p.add_argument('-v', action='store_true', default=None)
p.add_argument('-s', action='store_true', default=None)

results = p.parse_args()

base_dir = os.path.dirname(os.path.abspath(__file__))

# pythonpath
sys.path.append(os.path.join(base_dir, "modules"))

import SeleniumServer

# check if server is up
if not SeleniumServer.have_server():
  SeleniumServer.start_server()

c = Config()
# essentially we are going to remove the default discovery method and only use -a as the filter
c.workingDir = os.path.join(base_dir, "scripts")
# apparently you can't overwrite the compiled re, but can control what is used
c.testMatchPat = r'^.*$'

# load the built-in plugins; need the attr and xunit ones specifically
pm = nose.plugins.manager.BuiltinPluginManager()
pm.loadPlugins()
c.plugins = pm

# logging
log_name = os.path.join(base_dir, 'logs', "%s.xml" % time.strftime("%Y-%m-%d-%M-%S"))
sys.argv.extend(['--with-xunit', '--xunit-file', log_name])
print(log_name)
nose.core.run(config = c)

shutil.copy(log_name, os.path.join(base_dir, 'logs', 'latest.xml'))

if os.path.exists(os.path.join(base_dir, "third_party", "selenium", "server.pid")):
  SeleniumServer.stop_server()