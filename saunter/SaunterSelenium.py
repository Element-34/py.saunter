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
import saunter.ConfigWrapper
from saunter.exceptions import ElementNotFound

class SaunterSelenium(selenium):
    """
    Extending the regular selenium class to add implicit waits
    """
    def __init__(self, *args):
        super(SaunterSelenium, self).__init__(*args)
        
        try:
            if saunter.ConfigWrapper.ConfigWrapper().config.getboolean("Saunter", "use_implicit_wait"):
                self.implicit_wait = saunter.ConfigWrapper.ConfigWrapper().config.getint("Saunter", "implicit_wait")
            else:
                self.implicit_wait = 0
        except:
            self.implicit_wait = 0

    def do_command(self, verb, args, implicit_wait = None):
        if implicit_wait == None:
            implicit_wait = self.implicit_wait
            
        try:
            return super(SaunterSelenium, self).do_command(verb, args)
        except Exception, e:
            if (re.match("ERROR: Element .* not found", str(e))
                and implicit_wait > 0):
                time.sleep(1)
                return self.do_command(verb, args, implicit_wait - 1)
                        
            raise ElementNotFound(e)
            
    def click(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).click(locator)
        
    def double_click(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).double_click(locator)
        
    def context_menu(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).context_menu(locator)
        
    def click_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).click_at(locator, coordString)
        
    def double_click_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).double_click_at(locator, coordString)
        
    def context_menu_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).context_menu_at(locator, coordString)
        
    def fire_event(self, locator, eventName):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).fire_event(locator, eventName)
        
    def mouse_over(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_over(locator)
        
    def mouse_down(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_down(locator)
        
    def mouse_down_right(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_down_right(locator)
        
    def mouse_down_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_down_at(locator, coordString)
        
    def mouse_down_right_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_down_right_at(locator, coordString)
        
    def mouse_move(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_move(locator)
        
    def mouse_move_at(self, locator, coordString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).mouse_move_at(locator, coordString)
        
    def type(self, locator, value):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).type(locator, value)
        
    def type_keys(self, locator, value):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).type_keys(locator, value)
        
    def check(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).check(locator)
        
    def uncheck(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).uncheck(locator)
        
    def select(self, selectLocator, optionLocator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).select(selectLocator, optionLocator)
        
    def add_selection(self, locator, optionLocator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).add_selection(selectLocator, optionLocator)
        
    def remove_selection(self, locator, optionLocator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).remove_selection(selectLocator, optionLocator)
        
    def remove_all_selections(self, locator):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).remove_all_selections(locator)
        
    def drag_and_drop(self, locator, movementsString):
        super(SaunterSelenium, self).focus(locator)
        return super(SaunterSelenium, self).drag_and_drop(locator, movementsString)
        
    def drag_and_drop_to_object(self, locatorOfObjectToBeDragged, locatorOfDragDestinationObject):
        super(SaunterSelenium, self).focus(locator)        
        return super(SaunterSelenium, self).drag_and_drop_to_object(locatorOfObjectToBeDragged, locatorOfDragDestinationObject)