from saunter.po.webdriver.page import Page as SaunterPage
from saunter.po import timeout_seconds
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
import time

locators = {
    "throbber": 'id=v4-p180_throb'
}

class EBayWait(WebDriverWait):
    def until_not(self, method):
        """Calls the method provided with the driver as an argument until the \
        return value is False."""
        end_time = time.time() + self._timeout
        while(time.time() < end_time):
            try:
                value = method(self._driver)
                if value:
                    pass
            except NoSuchElementException:
                return True
            time.sleep(self._poll)
        raise TimeoutException()

class Page(SaunterPage):
    def wait_for_trobber_sync(self):
        w = EBayWait(self.driver, timeout_seconds)
        w.until(lambda x: x.find_element_by_id(locators["throbber"][3:]))
        w.until_not(lambda x: x.find_element_by_id(locators["throbber"][3:]))
        
        