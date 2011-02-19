"""
===============
BaseTextElement
===============
"""
from pages.BaseElement import BaseElement
from SeleniumWrapper import SeleniumWrapper as wrapper

class BaseTextElement(BaseElement):
    """
    Base element class for Text fields
    """

    def __set__(self, obj, val):
        wrapper().connection.type(self.locator, val)

    def __get__(self, obj, cls=None):
        try:
            return str(wrapper().connection.get_text(self.locator))
        except AttributeError as e:
            if str(e) == "'SeleniumWrapper' object has no attribute 'connection'":
                pass
            else:
                raise e
