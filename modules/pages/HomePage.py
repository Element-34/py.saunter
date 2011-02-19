"""
========
HomePage
========
"""
from pages import string_timeout
from pages.BasePage import BasePage
from pages.LoginPage import LoginPage
from SeleniumWrapper import SeleniumWrapper as wrapper

locators = {
    "login": "css=div.account_mast a:first",
    "signup": "css=div.account_mast a:last"
}

class HomePage(BasePage):
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
        