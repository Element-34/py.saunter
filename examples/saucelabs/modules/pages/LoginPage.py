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
=========
LoginPage
=========
"""
from saunter.po.page import Page
from saunter.po.text import Text
from saunter.po import string_timeout
from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

locators = {
    "username": "username",
    "password": "password",
    "submit_button": "submit",
    "error_message": "css=div.error p:nth(0)"
}

class UsernameTextElement(Text):
    def __init__(self):
        self.locator = locators["username"]

class PasswordTextElement(Text):
    def __init__(self):
        self.locator = locators["password"]

class ErrorMessageTextElement(Text):
    def __init__(self):
        self.locator = locators["error_message"]

class LoginPage(Page):
    """
    PO for the Login page
    """
    #: username text field
    username = UsernameTextElement()
    #: password text field
    password = PasswordTextElement()
    #: incorrect login message
    error_message = ErrorMessageTextElement()
    
    def __init__(self):
        self.se = wrapper().connection
        
    def do_login(self):
        """
        Does the form submission
        """
        self.se.click(locators['submit_button'])
        self.se.wait_for_page_to_load(string_timeout)