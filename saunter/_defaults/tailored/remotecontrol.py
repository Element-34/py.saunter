"""
=============
RemoteControl
=============
"""
from saunter.SaunterSelenium import SaunterSelenium

class RemoteControl(SaunterSelenium):
    """
    Modifications to the core Remote Control API are done in this class
    """
    def __init__(self, *args):
        super(RemoteControl, self).__init__(*args)