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
======
Common
======
"""

import saunter.ConfigWrapper

cf = saunter.ConfigWrapper.ConfigWrapper().config
#: timeout value in s as an integer
if cf.has_option("Selenium", "timeout"):
    timeout_seconds = cf.getint("Selenium", "timeout")
else:
    timeout_seconds = 30
#: timout value in ms as an integer
timeout_microseconds = timeout_seconds * 1000
#: timout value in ms as a string
string_timeout = str(timeout_microseconds)