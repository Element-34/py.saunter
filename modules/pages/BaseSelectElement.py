"""
=================
BaseSelectElement
=================
"""
from pages.BaseElement import BaseElement
from SeleniumWrapper import SeleniumWrapper as wrapper

class BaseSelectElement(BaseElement):
    """
    Base element class for Select fields
    """
    def __set__(self, obj, val):
        wrapper().connection.select(self.locator, val)

    def __get__(self, obj, cls=None):
        try:
            return str(wrapper().connection.get_selected_label(self.locator))
        except AttributeError as e:
            if str(e) == "'SeleniumWrapper' object has no attribute 'connection'":
                pass
            else:
                raise e
