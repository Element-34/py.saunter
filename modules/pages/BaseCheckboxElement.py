"""
===================
BaseCheckboxElement
===================
"""
from pages.BaseElement import BaseElement
from SeleniumWrapper import SeleniumWrapper as wrapper

class BaseCheckboxElement(BaseElement):
    """
    Base element class for Checkboxes
    """
    def __set__(self, obj, val):
        if (val == True and str(wrapper().connection.get_value(self.locator)) == 'off') or (val == False and str(wrapper().connection.get_value(self.locator)) == 'on'):
            wrapper().connection.click(self.locator)

    def __get__(self, obj, cls=None):
        try:
            return str(wrapper().connection.get_value(self.locator))
        except AttributeError as e:
            if str(e) == "'SeleniumWrapper' object has no attribute 'connection'":
                pass
            else:
                raise e
