from pages.BasePage import BasePage
from pages.BaseTextElement import BaseTextElement
from pages import string_timeout

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

    username = UsernameTextElement()
    password = PasswordTextElement()
    error_message = ErrorMessageTextElement()
    
    def __init__(self):
        super(LoginPage, self).__init__()
        
    def do_login(self):
        self.se.click(locators['submit_button'])
        self.se.wait_for_page_to_load(string_timeout)