from SeleniumWrapper import SeleniumWrapper

class BasePage(object):
    def __init__(self):
        self.se = SeleniumWrapper().connection