from pages.BaseElement import BaseElement

from SeleniumWrapper import SeleniumWrapper as wrapper

class BaseSelectElement(BaseElement):
    def __set__(self, obj, val):
        wrapper().connection.select(self.locator, val)

    def __get__(self, obj, cls=None):
        return str(wrapper().connection.get_selected_label(self.locator))
