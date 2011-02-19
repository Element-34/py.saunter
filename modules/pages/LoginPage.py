"""
=========
LoginPage
=========
"""
from pages.BasePage import BasePage
from pages.BaseTextElement import BaseTextElement
from pages import string_timeout
from SeleniumWrapper import SeleniumWrapper as wrapper

locators = {
    "username": "username",
    "password": "password",
    "submit_button": "submit",
    "error_message": "css=div.error p:nth(0)"
}

class UsernameTextElement(BaseTextElement):
    def __init__(self):
        self.locator = locators["username"]

class PasswordTextElement(BaseTextElement):
    def __init__(self):
        self.locator = locators["password"]

class ErrorMessageTextElement(BaseTextElement):
    def __init__(self):
        self.locator = locators["error_message"]

class LoginPage(BasePage):
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