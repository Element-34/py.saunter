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
import re
import time
from selenium import selenium

class SaunterSelenium(selenium):
    """
    Extending the regular selenium class to add implicit waits
    """

    def __init__(self, *args):
        self.implicit_wait = 30
        super(SaunterSelenium, self).__init__(*args)

    def do_command(self, verb, args, implicit_wait=None):
        if implicit_wait is None:
            implicit_wait = self.implicit_wait

        try:
            return super(SaunterSelenium, self).do_command(verb, args)
        except Exception, e:
            if (re.match("ERROR: Element .* not found", str(e))
                and implicit_wait > 0):
                time.sleep(1)
                return self.do_command(verb, args, implicit_wait-1)
            raise Exception(e)