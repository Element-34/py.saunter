import sys


class Matchers(object):
    def __init__(self, driver, verification_errors):
        self.driver = driver
        self.verification_erorrs = verification_errors

    #
    # unittest.TestCase provided
    #
    def assert_equal(self, first, second, msg=""):
        """
        Hard assert for equality

        :params first: the value to compare against
        :params second: the value to compare with
        :params msg: (Optional) msg explaining the difference
        """
        assert first == second

    def verify_equal(self, first, second, msg=""):
        """
        Soft assert for equality

        :params want: the value to compare against
        :params second: the value to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_equal(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_not_equal(self, first, second, msg=""):
        """
        Hard assert for inequality

        :params want: the value to compare against
        :params secondv: the value to compare with
        :params msg: (Optional) msg explaining the difference
        """
        assert first != second

    def verify_not_equal(self, first, second, msg=""):
        """
        Soft assert for inequality

        :params want: the value to compare against
        :params second: the value to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_not_equal(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_true(self, expr, msg=None):
        """
        Soft assert for whether the condition is true

        :params expr: the statement to evaluate
        :params msg: (Optional) msg explaining the difference
        """
        assert bool(expr) is True

    def verify_true(self, expr, msg=None):
        """
        Soft assert for whether the condition is true

        :params expr: the statement to evaluate
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_true(expr, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_false(self, expr, msg=None):
        """
        Soft assert for whether the condition is false

        :params expr: the statement to evaluate
        :params msg: (Optional) msg explaining the difference
        """
        assert bool(expr) is False

    def verify_false(self, expr, msg=None):
        """
        Soft assert for whether the condition is false

        :params expr: the statement to evaluate
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_false(expr, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is(self, first, second, msg=None):
        """
        Hard assert for whether the parameters evaluate to the same object

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        assert first is second

    def verify_is(self, first, second, msg=None):
        """
        Soft assert for whether the parameters evaluate to the same object

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is_not(self, first, second, msg=None):
        """
        Hard assert for whether the parameters do not evaluate to the same object

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        assert first is not second

    def verify_is_not(self, first, second, msg=None):
        """
        Soft assert for whether the parameters do not evaluate to the same object

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is_not(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is_none(self, expr, msg=None):
        """
        Hard assert for whether the expr is None

        :params expr: the expression to execute
        :params msg: (Optional) msg explaining the difference
        """
        assert expr is None

    def verify_is_none(self, expr, msg=None):
        """
        Soft assert for whether the expr is None

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is_none(expr, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is_not_none(self, expr, msg=None):
        """
        Hard assert for whether the expr is not None

        :params expr: the expression to execute
        :params msg: (Optional) msg explaining the difference
        """
        assert expr is not None

    def verify_is_not_none(self, expr, msg=None):
        """
        Soft assert for whether the expr is not None

        :params want: the object to compare against
        :params second: the object to compare with
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is_not_none(expr, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_in(self, first, second, msg=""):
        """
        Hard assert for whether the first is in second

        :params first: the value to check
        :params second: the container to check in
        :params msg: (Optional) msg explaining the difference
        """
        assert first in second

    def verify_in(self, first, second, msg=""):
        """
        Soft assert for whether the first is in second

        :params first: the value to check
        :params second: the container to check in
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_in(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_not_in(self, first, second, msg=""):
        """
        Hard assert for whether the first is not in second

        :params first: the value to check
        :params second: the container to check in
        :params msg: (Optional) msg explaining the difference
        """
        assert first not in second

    def verify_not_in(self, first, second, msg=""):
        """
        Soft assert for whether the first is not in second

        :params first: the value to check
        :params second: the container to check in
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_not_in(first, second, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is_instance(self, obj, cls, msg=""):
        """
        Hard assert for whether the is an instance of cls

        :params obj: the object instance
        :params cls: the class to compare against
        :params msg: (Optional) msg explaining the difference
        """
        assert isinstance(obj, cls)

    def verify_is_instance(self, obj, cls, msg=""):
        """
        Soft assert for whether the is an instance of cls

        :params obj: the object instance
        :params cls: the class to compare against
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is_instance(obj, cls, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_is_not_instance(self, obj, cls, msg=""):
        """
        Hard assert for whether the is not an instance of cls

        :params obj: the object instance
        :params cls: the class to compare against
        :params msg: (Optional) msg explaining the difference
        """
        assert not isinstance(obj, cls)

    def verify_is_not_instance(self, obj, cls, msg=""):
        """
        Soft assert for whether the is not an instance of cls

        :params obj: the object instance
        :params cls: the class to compare against
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_is_not_instance(obj, cls, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    #
    # selenium specific
    #
    def assert_text_present(self, text, msg=None):
        """
        Hard assert for whether the text if visible in the current window/frame

        :params text: the string to search for
        :params msg: (Optional) msg explaining the difference
        """
        e = driver.find_element_by_tag_name('body')
        assert text in e.text

    def verify_text_present(self, text, msg=None):
        """
        Soft assert for whether the text if visible in the current window/frame

        :params text: the string to search for
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_text_present(text, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def asset_element_present(self, locator, msg=None):
        """
        Hard assert for whether and element is present in the current window/frame

        :params locator: the locator of the element to search for
        :params msg: (Optional) msg explaining the difference
        """
        e = driver.find_elements_by_locator(locator)
        if len(e) == 0:
            raise AssertionError("Element at %s was not found" % locator)

    def verify_element_present(self, locator, msg=None):
        """
        Soft assert for whether and element is present in the current window/frame

        :params locator: the locator of the element to search for
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.asset_element_present(locator, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)

    def assert_visible(self, locator, msg=None):
        """
        Hard assert for whether and element is present and visible in the current window/frame

        :params locator: the locator of the element to search for
        :params msg: (Optional) msg explaining the difference
        """
        e = driver.find_elements_by_locator(locator)
        if len(e) == 0:
            raise AssertionError("Element at %s was not found" % locator)
        assert e.is_displayed()

    def verify_visible(self, locator, msg=None):
        """
        Soft assert for whether and element is present and visible in the current window/frame

        :params locator: the locator of the element to search for
        :params msg: (Optional) msg explaining the difference
        """
        try:
            self.assert_visible(locator, msg)
        except AssertionError, e:
            if msg:
                m = "%s:\n%s" % (msg, str(e))
            else:
                m = str(e)
            self.verification_erorrs.append(m)
