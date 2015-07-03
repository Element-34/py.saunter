import sys
from tailored.webdriver import WebDriver as TailoredWebDriver
from saunter.exceptions import ProfileNotFound
from selenium.webdriver import FirefoxProfile
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from saunter.matchers import Matchers

capabilities_map = {
    "firefox": DesiredCapabilities.FIREFOX,
    "internet explorer": DesiredCapabilities.INTERNETEXPLORER,
    "internetexplorer": DesiredCapabilities.INTERNETEXPLORER,
    "iexplore": DesiredCapabilities.INTERNETEXPLORER,
    "ie": DesiredCapabilities.INTERNETEXPLORER,
    "chrome": DesiredCapabilities.CHROME,
    "opera": DesiredCapabilities.OPERA,
    "chrome": DesiredCapabilities.CHROME,
    "htmlunitjs": DesiredCapabilities.HTMLUNITWITHJS,
    "htmlunit": DesiredCapabilities.HTMLUNIT,
    "iphone": DesiredCapabilities.IPHONE,
    "ipad": DesiredCapabilities.IPAD,
    "android": DesiredCapabilities.ANDROID,
    "phantomjs": DesiredCapabilities.PHANTOMJS,
}

os_map = {
    "XP": "XP",
    "Windows 2003": "XP",
    "VISTA": "VISTA",
    "Windows 2008": "VISTA",
    "Linux": "LINUX",
    "LINUX": "LINUX",
    "MAC": "MAC"
}

class Browser(TailoredWebDriver):
    def __init__(self, browser_config, all_config):
        self.browser_config = browser_config
        self.config = all_config

        profile = None
        if browser_config["type"] == 'firefox':
            if browser_config["profiles"][sys.platform]:
                profile_path = os.path.join(self.config["saunter"]["base"], 'support', 'profiles', browser_config["profiles"][sys.platform])
            elif browser_config["profiles"]["profile"]:
                profile_path = os.path.join(self.config["saunter"]["base"], 'support', 'profiles', browser_config["profiles"]["profile"])
            else:
                profile_path = None

            if profile_path:
                if os.path.isdir(profile_path):
                    profile = FirefoxProfile(profile_path)
                else:
                    raise ProfileNotFound("Profile not found at %s" % profile_path)

        if browser_config["sauce labs"]["ondemand"]:
            desired_capabilities = {
                "platform": browser_config["sauce labs"]["os"],
                "browserName": browser_config["type"],
                "version": browser_config["sauce labs"]["version"],
            }
            if desired_capabilities["platform"] in os_map:
                desired_capabilities["platform"] = os_map[desired_capabilities["platform"]]

            if 'selenium version' in browser_config['sauce labs'] and \
                len(browser_config['sauce labs']['selenium version']) > 0:
                desired_capabilities['selenium-version'] = browser['sauce labs']['selenium version']

            if "disable" in self.config["sauce labs"] and self.config["sauce labs"]["disable"] is not None:
                if "record video" in self.config["sauce labs"]["disable"]:
                    if self.config["sauce labs"]["disable"]["record video"] == True:
                        desired_capabilities['record-video'] = False
                if "upload video on pass" in self.config["sauce labs"]["disable"]:
                    if self.config["sauce labs"]["disable"]["upload video on pass"] == True:
                        desired_capabilities['video-upload-on-pass'] = False
                if "step screenshots" in self.config["sauce labs"]["disable"]:
                    if self.config["sauce labs"]["disable"]["step screenshots"] == True:
                        desired_capabilities['record-screenshots'] = False
                if "sauce advisor" in self.config["sauce labs"]["disable"]:
                    if self.config["sauce labs"]["disable"]["sauce advisor"] == True:
                        desired_capabilities['sauce-advisor'] = False

            if "enable" in self.config["sauce labs"] and self.config["sauce labs"]["enable"] is not None:
                if "source capture" in self.config["sauce labs"]["enable"]:
                    if self.config["sauce labs"]["enable"]["source capture"] == True:
                        desired_capabilities['source capture'] = True
                if "error screenshots" in self.config["sauce labs"]["enable"]:
                    if self.config["sauce labs"]["enable"]["error screenshots"] == True:
                        desired_capabilities['webdriver.remote.quietExceptions'] = True

            command_executor = "http://%s:%s@ondemand.saucelabs.com:80/wd/hub" % (self.config["sauce labs"]["username"], self.config["sauce labs"]["key"])
        else:
            desired_capabilities = capabilities_map[browser_config["type"]]

            if 'type' in self.config['selenium']['proxy'] and \
                self.config['selenium']['proxy']['type'] is not None and \
                self.config['selenium']['proxy']['type'].lower() == "browsermob":
                
                self.proxy = self.config['saunter']['proxies'].pop()
                self.proxy.add_to_webdriver_capabilities(desired_capabilities)

            if "is grid" in self.config["selenium"] and self.config["selenium"]["executor"]["is grid"]:
                    if browser_config["grid filters"]["platform"]:
                        desired_capabilities["platform"] = browser_config["grid filters"]["platform"].upper()
                    if browser_config["grid filters"]["version"]:
                        desired_capabilities["platform"] = str(browser_config["grid filters"]["version"])

            command_executor = "http://%s:%s/wd/hub" % (self.config["selenium"]["executor"]["host"], self.config["selenium"]["executor"]["port"])

        # print(desired_capabilities)
        self.driver = TailoredWebDriver(desired_capabilities=desired_capabilities, command_executor=command_executor, browser_profile=profile)
