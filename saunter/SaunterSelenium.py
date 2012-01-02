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
    Extending the regular selenium class to add implicit waits
    """
    def __init__(self, *args):
        super(SaunterSelenium, self).__init__(*args)
        
        self.cf = saunter.ConfigWrapper.ConfigWrapper().config
        self.screenshots_where = os.path.join(self.cf.get("Saunter", "base"), "logs", self.cf.get("Saunter", "name"))
        if os.path.exists(self.screenshots_where):
            shutil.rmtree(self.screenshots_where)
        os.makedirs(self.screenshots_where)
        self.screenshot_number = 1
        
        try:
            if cf.getboolean("Saunter", "use_implicit_wait"):
                self.implicit_wait = cf.getint("Saunter", "implicit_wait")
            else:
                self.implicit_wait = 0
        except:
            self.implicit_wait = 0
        
    def stop(self):
        super(SaunterSelenium, self).stop()
        self.running = False

    def do_command(self, verb, args, implicit_wait = None):
        if implicit_wait == None:
            implicit_wait = self.implicit_wait
            
        try:
            return super(SaunterSelenium, self).do_command(verb, args)
        except Exception, e:
            if (re.match("ERROR: Element .* not found", unicode(e))
                and implicit_wait > 0):
                time.sleep(1)
                return self.do_command(verb, args, implicit_wait - 1)
            elif (re.match("ERROR: Element .* not found", unicode(e))
                and implicit_wait == 0):
                self.take_numbered_screenshot()
                raise ElementNotFound(e)
                
            if (re.match("ERROR: Could not find window with .*", unicode(e))
                and implicit_wait > 0):
                time.sleep(1)
                return self.do_command(verb, args, implicit_wait - 1)
            elif (re.match("ERROR: Could not find window with .*", unicode(e))
                and implicit_wait == 0):
                self.take_numbered_screenshot()
                raise WindowNotFound(e)
            raise Exception(unicode(e))
    
    def take_numbered_screenshot(self):
        if self.cf.has_option("Saunter", "take_screenshots"):
            if self.cf.getboolean("Saunter", "take_screenshots"):
                super(SaunterSelenium, self).capture_screenshot(os.path.join(self.screenshots_where, str(self.screenshot_number).zfill(3) + ".png"))
                self.screenshot_number = self.screenshot_number + 1

    def take_named_screenshot(self, name):
        super(SaunterSelenium, self).capture_screenshot(os.path.join(self.screenshots_where, str(name) + ".png"))

    def click(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).click(locator)
        self.take_numbered_screenshot()
        
    def double_click(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).double_click(locator)
        self.take_numbered_screenshot()

    def check(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).check(locator)
        self.take_numbered_screenshot()

    def click_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).click_at(locator, coordString)
        self.take_numbered_screenshot()

    def context_menu(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).context_menu(locator)
        self.take_numbered_screenshot()

    def context_menu_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).context_menu_at(locator, coordString)
        self.take_numbered_screenshot()
        
    def double_click_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).double_click_at(locator, coordString)
        self.take_numbered_screenshot()

    def drag_and_drop(self, locator, movementsString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).drag_and_drop(locator, movementsString)
        self.take_numbered_screenshot()

    def drag_and_drop_to_object(self, locatorOfObjectToBeDragged, locatorOfDragDestinationObject, focus_before = True):
        if focus_before:
            self.focus(locatorOfObjectToBeDragged)
        super(SaunterSelenium, self).drag_and_drop_to_object(locatorOfObjectToBeDragged, locatorOfDragDestinationObject)
        self.take_numbered_screenshot()
    
    def focus(self, locator):
        try:
            super(SaunterSelenium, self).focus(locator)
        except:
            pass
            
    def fire_event(self, locator, eventName, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).fire_event(locator, eventName)
        self.take_numbered_screenshot()
        
    def mouse_over(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_over(locator)
        self.take_numbered_screenshot()
        
    def mouse_down(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down(locator)
        self.take_numbered_screenshot()
        
    def mouse_down_right(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_right(locator)
        self.take_numbered_screenshot()
        
    def mouse_down_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_at(locator, coordString)
        self.take_numbered_screenshot()
        
    def mouse_down_right_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_down_right_at(locator, coordString)
        self.take_numbered_screenshot()
        
    def mouse_move(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_move(locator)
        self.take_numbered_screenshot()
        
    def mouse_move_at(self, locator, coordString, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).mouse_move_at(locator, coordString)
        self.take_numbered_screenshot()

    def open(self, url, ignoreResponseCode=True):
        super(SaunterSelenium, self).open(url, ignoreResponseCode=True)
        self.take_numbered_screenshot()

    def open_window(self, url, windowID):
        super(SaunterSelenium, self).open_window(url, windowID)
        self.take_numbered_screenshot()

    def select(self, selectLocator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(selectLocator)
        super(SaunterSelenium, self).select(selectLocator, optionLocator)
        self.take_numbered_screenshot()
        
    def add_selection(self, locator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).add_selection(selectLocator, optionLocator)
        self.take_numbered_screenshot()
        
    def remove_selection(self, locator, optionLocator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).remove_selection(selectLocator, optionLocator)
        self.take_numbered_screenshot()
        
    def remove_all_selections(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).remove_all_selections(locator)
        self.take_numbered_screenshot()

    def submit(self, formLocator):
        super(SaunterSelenium, self).submit(formLocator)
        self.take_numbered_screenshot()

    def type(self, locator, value, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).type(locator, value)
        self.take_numbered_screenshot()

    def type_keys(self, locator, value, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).type_keys(locator, value)
        self.take_numbered_screenshot()

    def uncheck(self, locator, focus_before = True):
        if focus_before:
            self.focus(locator)
        super(SaunterSelenium, self).uncheck(locator)
        self.take_numbered_screenshot()

    def wait_for_condition(self, script, timeout):
        super(SaunterSelenium, self).wait_for_condition(script, timeout)
        self.take_numbered_screenshot()

    def wait_for_frame_to_load(self, frameAddress, timeout):
        super(SaunterSelenium, self).wait_for_frame_to_load(frameAddress, timeout)
        self.take_numbered_screenshot()

    def wait_for_page_to_load(self, timeout):
        super(SaunterSelenium, self).wait_for_page_to_load(timeout)
        self.take_numbered_screenshot()
        
    def wait_for_pop_up(self, windowID, timeout):
        super(SaunterSelenium, self).wait_for_pop_up(windowID, timeout)
        self.take_numbered_screenshot()
