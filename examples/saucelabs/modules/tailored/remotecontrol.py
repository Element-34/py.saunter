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
RemoteControl
=============
"""
from saunter.SaunterSelenium import SaunterSelenium

class RemoteControl(SaunterSelenium):
    """
    Modifications to the core Remote Control API are done in this class
    """
    def __init__(self, *args):
        super(RemoteControl, self).__init__(*args)
        
    def click(self, locator):
        """
        This does nothing but pass the command up the stack to the existing command
        """
        super(RemoteControl, self).click(locator)
    
    def triple_click(self, locator):
        """
        This command doesn't exist in the RemoteControl API
        """
        print("should be here")

    def quadruple_click(self, locator):
        """
        This does something, and then the original call
        """
        print("should be here")
        super(RemoteControl, self).click(locator)