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
from saunter.exceptions import ElementNotFound
from saunter.SaunterWebDriver import SaunterWebDriver
from selenium.webdriver.support.select import Select as WebDriverSelect
import saunter.exceptions

class Select(Element, WebDriverSelect):
    """
    Base element class for Select fields
    """    
    def __set__(self, obj, val):
        s = WebDriverSelect(obj.driver.find_element_by_locator(self.locator))
        method = val[:val.find("=")]
        value = val[val.find("=") + 1:]
        if method == "value":
            s.select_by_value(value)
        elif method == "index":
            s.select_by_index(value)
        elif method == "text":
            s.select_by_visible_text(value)
        else:
            raise saunter.exceptions.InvalidLocatorString(val)
    
    def __get__(self, obj, cls=None):
        try:
            s = WebDriverSelect(obj.driver.find_element_by_locator(self.locator))
            e = s.first_selected_option
            return str(e.text)
        except AttributeError as e:
            if str(e) == "'SeleniumWrapper' object has no attribute 'connection'":
                pass
            else:
                raise e

class Select2(Element, WebDriverSelect):
    def __init__(self, driver, locator):
        self.driver = driver
        self.locator = locator
    
    @property
    def selected(self):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        e = s.first_selected_option
        return str(e.text)

    @selected.setter
    def selected(self, val):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        method = val[:val.find("=")]
        value = val[val.find("=") + 1:]
        if method == "value":
            s.select_by_value(value)
        elif method == "index":
            s.select_by_index(value)
        elif method == "text":
            s.select_by_visible_text(value)
        else:
            raise saunter.exceptions.InvalidLocatorString(val)

    @property
    def options(self):
        s = WebDriverSelect(self.driver.find_element_by_locator(self.locator))
        options = s.options
        text = [option.text.strip() for option in options]
        return text
