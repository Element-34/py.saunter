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

import saunter.exceptions
from selenium import webdriver
from saunter.SeleniumWrapper import SeleniumWrapper as se_wrapper
from selenium.common.exceptions import NoSuchElementException

class SaunterWebDriver(webdriver.Remote):
    def find_element_by_locator(self, locator):
        locator_type = locator[:locator.find("=")]
        if locator_type == "":
            raise saunter.exceptions.InvalidLocatorString(locator)
        locator_value = locator[locator.find("=") + 1:]
        if locator_type == 'class':
            return self.find_element_by_class_name(locator_value)
        elif locator_type == 'css':
            return self.find_element_by_css_selector(locator_value)
        elif locator_type == 'id':
            return self.find_element_by_id(locator_value)
        elif locator_type == 'link':
            return self.find_element_by_link_text(locator_value)
        elif locator_type == 'name':
            return self.find_element_by_name(locator_value)
        elif locator_type == 'plink':
            return self.find_element_by_partial_link_text(locator_value)
        elif locator_type == 'tag':
            return self.find_element_by_tag_name(locator_value)
        elif locator_type == 'xpath':
            return self.find_element_by_xpath(locator_value)
        else:
            raise saunter.exceptions.InvalidLocatorString(locator)

    def find_elements_by_locator(self, locator):
        locator_type = locator[:locator.find("=")]
        if locator_type == "":
            raise saunter.exceptions.InvalidLocatorString(locator)
        locator_value = locator[locator.find("=") + 1:]
        if locator_type == 'class':
            return self.find_elements_by_class_name(locator_value)
        elif locator_type == 'css':
            return self.find_elements_by_css_selector(locator_value)
        elif locator_type == 'id':
            return self.find_elements_by_id(locator_value)
        elif locator_type == 'link':
            return self.find_elements_by_link_text(locator_value)
        elif locator_type == 'name':
            return self.find_elements_by_name(locator_value)
        elif locator_type == 'plink':
            return self.find_elements_by_partial_link_text(locator_value)
        elif locator_type == 'tag':
            return self.find_elements_by_tag_name(locator_value)
        elif locator_type == 'xpath':
            return self.find_elements_by_xpath(locator_value)
        else:
            raise saunter.exceptions.InvalidLocatorString(locator)

    # @deprecated
    @classmethod
    def click(cls, locator):
        driver = se_wrapper().connection
        
        e = cls.find_element_by_locator(locator)
        e.click()
        
    def is_element_present(self, locator):
        try:
            self.find_element_by_locator(locator)
            return True
        except NoSuchElementException:
            return False
    
    def is_visible(self, locator):
        return self.find_element_by_locator(locator).is_displayed()