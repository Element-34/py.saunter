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
Select
======
"""
from saunter.po.webdriver.element import Element
from saunter.web_element import WebElement
from saunter.SeleniumWrapper import SeleniumWrapper as wrapper
from saunter.exceptions import ElementNotFound
from saunter.SaunterWebDriver import SaunterWebDriver
from selenium.webdriver.support.select import Select as WebDriverSelect


class MultiSelect(Element, WebDriverSelect):
    def __get__(self, obj, cls=None):
        s = WebDriverSelect(obj.driver.find_element_by_locator(self.locator))
        a = s.all_selected_options
        if len(a) == 0:
            return None
        return [x.text for x in a]

    def __getitem__(self, key):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        a = s.all_selected_options
        if len(a) == 0:
            return None
        selections = [x.text for x in a]
        return selections[key]

    def __delitem__(self, key):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        method = key[:key.find("=")]
        value = key[key.find("=") + 1:]
        if method == "value":
            s.deselect_by_value(value)
        elif method == "index":
            s.deselect_by_index(value)
        elif method == "text":
            s.deselect_by_visible_text(value)
        else:
            raise saunter.exceptions.InvalidLocatorString("%s is an invalid locator" % item)

    def __len__(self):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        return len(s.all_selected_options)

    def append(self, item):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        method = item[:item.find("=")]
        value = item[item.find("=") + 1:]
        if method == "value":
            s.select_by_value(value)
        elif method == "index":
            s.select_by_index(value)
        elif method == "text":
            s.select_by_visible_text(value)
        else:
            raise saunter.exceptions.InvalidLocatorString("%s is an invalid locator" % item)
