import unittest2 as unittest

class BaseTestCase(unittest.TestCase):
    def verify_equal(self, want, got):
        try:
            self.assertEqual(want, got)
        except AssertionError, e:
            self.verificationErrors.append(str(e))

    def verify_text_present(self, text):
        try:
            self.assertTrue(self.selenium.is_text_present(text))
        except AssertionError, e:
            self.verificationErrors.append(str(e))

    def verify_element_present(self, locator):
        try:
            self.assertTrue(self.selenium.is_element_present(locator))
        except AssertionError, e:
            self.verificationErrors.append(str(e))

    def verify_visible(self, locator):
        try:
            self.assertTrue(self.selenium.is_visible(locator))
        except AssertionError, e:
            self.verificationErrors.append(str(e))

    def verify_true(self, condition):
        try:
            self.assertTrue(condition)
        except AssertionError, e:
            self.verificationErrors.append(str(e))