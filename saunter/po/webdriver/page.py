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
====
Page
====
"""
from saunter.po import timeout_seconds
import saunter.exceptions
import time
from saunter.SaunterWebDriver import SaunterWebDriver
from selenium.common.exceptions import StaleElementReferenceException

class Page(object):
    """
    Top of the PO page tree
    """
    def is_element_available(self, locator):
        """
        Synchronization method for making sure the element we're looking for is not only on the page,
        but also visible -- since Se will happily deal with things that aren't visible.
        
        Use this instead of is_element_present most of the time.
        """
        if SaunterWebDriver.is_element_present(locator):
            if SaunterWebDriver.is_visible(locator):
                return True
            else:
                return False
        else:
            return False

    def wait_for_available(self, locator):
        """
        Synchronization to deal with elements that are present, and are visible

        :raises: ElementVisiblityTimeout        
        """
        for i in range(timeout_seconds):
            try:
                if self.is_element_available(locator):
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementVisiblityTimeout("%s availability timed out" % locator)
        return True
            
    def wait_for_visible(self, locator):
        """
        Synchronization to deal with elements that are present, but are disabled until some action
        triggers their visibility.
        
        :raises: ElementVisiblityTimeout        
        """
        for i in range(timeout_seconds):
            try:
                if SaunterWebDriver.is_visible(locator):
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementVisiblityTimeout("%s visibility timed out" % locator)
        return True

    def wait_for_hidden(self, locator):
        """
        Synchronization to deal with elements that are present, but are visibility until some action
        triggers their hidden-ness.

        :raises: ElementVisiblityTimeout=
        """
        for i in range(timeout_seconds):
            if SaunterWebDriver.is_visible(locator):
                time.sleep(1)
            else:
                break
        else:
            raise ElementVisiblityTimeout("%s visibility timed out" % locator)
        return True
            
    def wait_for_text(self, locator, text):
        """
        Synchronization on some text being displayed in a particular element.

        :raises: ElementVisiblityTimeout
        """
        for i in range(timeout_seconds):
            try:
                e = SaunterWebDriver.find_element_by_locator(locator)
                if e.text == text:
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementTextTimeout("%s value timed out" % locator)
        return True

    def wait_for_value(self, locator, text):
        """
        Synchronization on some value being set in a particular element.

        :raises: ElementVisiblityTimeout

        """
        for i in range(timeout_seconds):
            try:
                e = SaunterWebDriver.find_element_by_locator(locator)
                if e.value ==text:
                    break
            except:
                pass
            time.sleep(1)
        else:
            raise ElementTextTimeout("%s value timed out" % locator)
        return True

    def wait_for_value_changed(self, locator, text):
        e = SaunterWebDriver.find_element_by_locator(locator)
        for i in range(timeout_seconds):
            try:
                if len(e.text.strip()) != 0 and e.text != text:
                    return True
            except StaleElementReferenceException, e:
                e = SaunterWebDriver.find_element_by_locator(locator)
            finally:
                time.sleep(1)
        else:
            raise saunter.exceptions.ElementVisiblityTimeout("%s visibility timed out" % locator)

    def wait_for_element_not_present(self, locator):
        """
        Synchronization helper to wait until some element is removed from the page 

        :raises: ElementVisiblityTimeout
        """
        for i in range(timeout_seconds):
            if SaunterWebDriver.is_element_present(locator):
                time.sleep(1)
            else:
                break
        else:
            raise ElementVisiblityTimeout("%s presence timed out" % locator)
        return True