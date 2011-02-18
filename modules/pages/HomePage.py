from pages import string_timeout
from pages.BasePage import BasePage
from pages.LoginPage import LoginPage

locators = {
    "login": "css=div.account_mast a:first",
    "signup": "css=div.account_mast a:last"
}

class HomePage(BasePage):
    def __init__(self):
        super(HomePage, self).__init__()

    def open_default_url(self):
        self.se.open("/")
    
    def go_to_login_page(self):
        self.se.click(locators['login'])
        self.se.wait_for_page_to_load(string_timeout)
        return LoginPage()
        