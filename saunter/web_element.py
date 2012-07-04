from selenium.webdriver.remote.webelement import WebElement
import saunter.exceptions

class WebElement(WebElement):
    def __init__(self, element):
        self.__dict__.update(element.__dict__)
        
    def find_element_by_locator(self, locator):
        locator_type = locator[:locator.find("=")]
        if locator_type == "":
            raise saunter.exceptions.InvalidLocatorString(locator)
        locator_value = locator[locator.find("=") + 1:]
        if locator_type == 'class':
            return self.find_element_by_class_name(locator_value)
        elif locator_type == 'css':
            return self.find_element_by_css_selector(locator_value)
        elif locator_type == 'id':
            return self.find_element_by_id(locator_value)
        elif locator_type == 'link':
            return self.find_element_by_link_text(locator_value)
        elif locator_type == 'name':
            return self.find_element_by_name(locator_value)
        elif locator_type == 'plink':
            return self.find_element_by_partial_link_text(locator_value)
        elif locator_type == 'tag':
            return self.find_element_by_tag_name(locator_value)
        elif locator_type == 'xpath':
            return self.find_element_by_xpath(locator_value)
        else:
            raise saunter.exceptions.InvalidLocatorString(locator)