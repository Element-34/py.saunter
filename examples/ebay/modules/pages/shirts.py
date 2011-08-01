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
from saunter.po.page import Page
from saunter.po.text import Text
from saunter.po import string_timeout, timeout_seconds
from saunter.SeleniumWrapper import SeleniumWrapper as wrapper
from saunter.exceptions import ElementVisiblityTimeout
import time

locators = {
    "collar style": 'css=a[title="REPLACE"]',
    "results": 'css=.count',
    "throbber": 'id=PreferenceThrob'
}

class ResultsTextElement(Text):
    def __init__(self):
        self.locator = locators["results"]

class ShirtPage(Page):
    results = ResultsTextElement()
    
    def __init__(self):
        self.se = wrapper().connection
        
    def go_to_mens_dress_shirts(self):
        self.se.open("/mens-clothing/Dress-Shirts/57991")
        self.se.wait_for_page_to_load(string_timeout)
        
    def change_collar_style(self, style):
        before = self.results;
        self.se.click(locators["collar style"].replace("REPLACE", style))
        self.wait_for_value_changed(locators["results"], self.results)
        
    def is_collar_selected(self, style):
        if self.se.is_element_present("%s .sl-deSel" % locators["collar style"].replace("REPLACE", style)):
            return False
        return True
        