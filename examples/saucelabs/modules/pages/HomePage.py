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
========
HomePage
========
"""
from saunter.po import string_timeout
from saunter.po.page import Page
from pages.LoginPage import LoginPage
from saunter.SeleniumWrapper import SeleniumWrapper as wrapper

locators = {
    "login": "css=div.account_mast a:first",
    "signup": "css=div.account_mast a:last"
}

class HomePage(Page):
    """
    PO for the Home/Landing page
    """
    def __init__(self):
        self.se = wrapper().connection

    def open_default_url(self):
        """
        Goes to the default url for this PO
        """
        self.se.open("/")
    
    def go_to_login_page(self):
        """
        Goes to the login page
        
        :returns: :class:`pages.LoginPage.LoginPage`
        """
        self.se.click(locators['login'])
        self.se.wait_for_page_to_load(string_timeout)
        return LoginPage()
        