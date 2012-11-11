"""
=============
WebDriver
=============
"""
from saunter.SaunterWebDriver import SaunterWebDriver

class WebDriver(SaunterWebDriver):
    """
    Modifications to the core WebDriver API are done in this class
    """
    def __init__(self, **kwargs):
        super(WebDriver, self).__init__(**kwargs)

