from pages.BaseElement import BaseElement

from SeleniumWrapper import SeleniumWrapper as wrapper

class BaseTextElement(BaseElement):
    def __set__(self, obj, val):
        wrapper().connection.type(self.locator, val)

    def __get__(self, obj, cls=None):
        return str(wrapper().connection.get_text(self.locator))
