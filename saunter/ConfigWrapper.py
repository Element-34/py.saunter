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
=============
ConfigWrapper
=============
"""
import ConfigParser
import os
import os.path

class ConfigWrapper(object):
    """
    Singleton reference to the config information
    """
    # singleton
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigWrapper, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def configure(self, config = "saunter.ini"):
        self.config = ConfigParser.SafeConfigParser()
        self.config.readfp(open(os.path.join("conf", config)))

# initialize the singleton
try:
    cf = ConfigWrapper().configure()
except IOError as e:
    if "DOCGENERATION" not in os.environ:
        raise