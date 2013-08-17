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
import os
import os.path
import sys
import yaml

class ConfigWrapper(object):
    """
    Singleton reference to the config information
    """
    # singleton
    _instance = None
    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ConfigWrapper, cls).__new__(cls, *args, **kwargs)
            cls._instance._data = {}
        return cls._instance

    def __str__(self):
        return yaml.dump(self._data, default_flow_style=False)

    def __getitem__(self, key):
        return self._data[key]

    def __setitem__(self, key, value):
        self._data[key] = value

    def __contains__(self, item):
        if item in self._data:
            return True
        return False

    def configure(self, config = "saunter.yaml"):
        if not os.path.exists(os.path.join("conf", config)):
            print("Could not find %s; are you sure you remembered to create one?" % os.path.join("conf", config))
            sys.exit(1)

        # this should exist since configure() is only called in main.py
        config_dir = os.path.join(self._data["saunter"]["base"], "conf")
        for root, dirs, files in os.walk(config_dir):
            for f in files:
                if f.endswith(".yaml"):
                    file_path = os.path.join(root, f)
                    relative_path = file_path[len(config_dir) + 1:]
                    head, tail = os.path.split(relative_path)
                    section_name = f[:-5]
                    o = open(file_path, "r")
                    if head:
                        if head not in self._data.keys():
                            self._data[head] = {}
                        if section_name in self._data[head]:
                            self._data[head][section_name] = dict(self._data[head][section_name].items() + yaml.load(o).items())
                        else:
                            self._data[head][section_name] = yaml.load(o)
                    else:
                        if section_name in self._data:
                            self._data[section_name] = dict(self._data[section_name].items() + yaml.load(o).items())
                        else:
                            self._data[section_name] = yaml.load(o)
                    o.close()
