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
import os
import os.path
import re
import shutil
import time
from selenium import selenium
import saunter.ConfigWrapper
from saunter.exceptions import ElementNotFound, WindowNotFound

class SaunterSelenium(selenium):
    """
    Extending the Se-RC driver
    """
    def __init__(self, *args):
        super(SaunterSelenium, self).__init__(*args)
        
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        
    def stop(self):
        super(SaunterSelenium, self).stop()
        self.running = False

    def do_command(self, verb, args):
        try:
            return super(SaunterSelenium, self).do_command(verb, args)
        except Exception, e:
            if (re.match("ERROR: Element .* not found", unicode(e))):
                raise ElementNotFound(e)
                
            if (re.match("ERROR: Could not find window with .*", unicode(e))):
                raise WindowNotFound(e)
            raise Exception(unicode(e))

    def click(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).click(locator)
        
    def double_click(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).double_click(locator)

    def check(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).check(locator)

    def click_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).click_at(locator, coordString)

    def context_menu(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).context_menu(locator)

    def context_menu_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).context_menu_at(locator, coordString)
        
    def double_click_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).double_click_at(locator, coordString)

    def drag_and_drop(self, locator, movementsString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).drag_and_drop(locator, movementsString)

    def drag_and_drop_to_object(self, locatorOfObjectToBeDragged, locatorOfDragDestinationObject, focus_before = True):
        if focus_before:
            self.focus(locatorOfObjectToBeDragged)
        super(SaunterSelenium, self).drag_and_drop_to_object(locatorOfObjectToBeDragged, locatorOfDragDestinationObject)
    
    def focus(self, locator):
        try:
            super(SaunterSelenium, self).focus(locator)
        except:
            pass
            
    def fire_event(self, locator, eventName, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).fire_event(locator, eventName)
        
    def mouse_over(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_over(locator)
        
    def mouse_down(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down(locator)
        
    def mouse_down_right(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_right(locator)
        
    def mouse_down_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_at(locator, coordString)
        
    def mouse_down_right_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_right_at(locator, coordString)
        
    def mouse_move(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_move(locator)
        
    def mouse_move_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_move_at(locator, coordString)

    def open(self, url, ignoreResponseCode=True):
        super(SaunterSelenium, self).open(url, ignoreResponseCode=True)

    def open_window(self, url, windowID):
        super(SaunterSelenium, self).open_window(url, windowID)

    def select(self, selectLocator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(selectLocator)
        super(SaunterSelenium, self).select(selectLocator, optionLocator)
        
    def add_selection(self, locator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).add_selection(selectLocator, optionLocator)
        
    def remove_selection(self, locator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).remove_selection(selectLocator, optionLocator)
        
    def remove_all_selections(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).remove_all_selections(locator)

    def submit(self, formLocator):
        super(SaunterSelenium, self).submit(formLocator)

    def type(self, locator, value, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).type(locator, value)

    def type_keys(self, locator, value, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).type_keys(locator, value)

    def uncheck(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).uncheck(locator)

    def wait_for_condition(self, script, timeout):
        super(SaunterSelenium, self).wait_for_condition(script, timeout)

    def wait_for_frame_to_load(self, frameAddress, timeout):
        super(SaunterSelenium, self).wait_for_frame_to_load(frameAddress, timeout)

    def wait_for_page_to_load(self, timeout):
        super(SaunterSelenium, self).wait_for_page_to_load(timeout)
        
    def wait_for_pop_up(self, windowID, timeout):
        super(SaunterSelenium, self).wait_for_pop_up(windowID, timeout)
