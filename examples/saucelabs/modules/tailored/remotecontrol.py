from saunter.SaunterSelenium import SaunterSelenium

class RemoteControl(SaunterSelenium):
    def __init__(self, *args):
        super(RemoteControl, self).__init__(*args)
        
    def click(self, locator):
        """
        This does nothing but pass the command up the stack to the existing command
        """
        super(RemoteControl, self).click(locator)
    
    def triple_click(self, locator):
        """
        This command doesn't exist in the RemoteControl API
        """
        print("should be here")

    def quadruple_click(self, locator):
        """
        This does something, and then the original call
        """
        print("should be here")
        super(RemoteControl, self).click(locator)