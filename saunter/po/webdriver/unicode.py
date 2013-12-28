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
=======
Unicode
=======
"""
from saunter.po.webdriver.element import Element
from saunter.SeleniumWrapper import SeleniumWrapper as wrapper
from saunter.exceptions import ElementNotFound
from saunter.SaunterWebDriver import SaunterWebDriver


class Unicode(Element):
    """
    Base element class for Unicode fields
    """
    def __set__(self, obj, val):
        e = obj.driver.find_element_by_locator(self.locator)
        e.send_keys(val)

    def __get__(self, obj, cls=None):
        e = obj.driver.find_element_by_locator(self.locator)
        if e.tag_name in ["input", "textarea"]:
            return e.get_attribute("value")
        return e.text
