import saunter.exceptions
from selenium import webdriver
from saunter.SeleniumWrapper import SeleniumWrapper as se_wrapper
from selenium.common.exceptions import NoSuchElementException

class SaunterWebDriver(object):
    @classmethod
    def find_element_by_locator(cls, locator):
        driver = se_wrapper().connection
        
        locator_type = locator[:locator.find("=")]
        if locator_type == "":
            raise saunter.exceptions.InvalidLocatorString(locator)
        locator_value = locator[locator.find("=") + 1:]
        if locator_type == 'class':
            return driver.find_element_by_class_name(locator_value)
        elif locator_type == 'css':
            return driver.find_element_by_css_selector(locator_value)
        elif locator_type == 'id':
            return driver.find_element_by_id(locator_value)
        elif locator_type == 'link':
            return driver.find_element_by_link_text(locator_value)
        elif locator_type == 'name':
            return driver.find_element_by_name(locator_value)
        elif locator_type == 'plink':
            return driver.find_element_by_partial_link_text(locator_value)
        elif locator_type == 'tag':
            return driver.find_element_by_tag_name(locator_value)
        elif locator_type == 'xpath':
            return driver.find_element_by_xpath(locator_value)
        else:
            raise saunter.exceptions.InvalidLocatorString(locator)
            
    @classmethod
    def click(cls, locator):
        driver = se_wrapper().connection
        
        e = cls.find_element_by_locator(locator)
        e.click()
        
    @classmethod
    def is_element_present(cls, locator):
        try:
            cls.find_element_by_locator(locator)
            return True
        except NoSuchElementException:
            return False
    
    @classmethod
    def is_visible(cls, locator):
        return cls.find_element_by_locator(locator).is_displayed()