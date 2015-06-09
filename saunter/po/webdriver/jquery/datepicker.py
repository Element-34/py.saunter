from saunter.po.webdriver.element import Element

class NoSuchDayException(Exception):
    """ Custom exception for trying to select an invalid day of the month
    
    Rather than try and be clever around which days are valid in a month, we trust that
    the widget is populating things correctly and just blow up if you request the 4th day
    of the month for instance.
    """
    pass

class DatePicker(Element):
    """ Helper class for dealing with JQueryUI Datepicker controls/widgets/whatever """    

    def __set__(self, obj, val):
        """ Navigate through the datepicker control and select the date
        
        Using named arguments rather than try and dictate a specific date format. If
        someone wants to format things a specific way they can wrap this class and parse
        their input before passing it along here
        """
        _how_many_clicks = 0

        # this is the input field that the datepicker control is attached to (in this
        # standalone example it doesn't make sense, but in the larger framework it does...)
        click_to_open = obj.driver.find_element_by_locator(self.locator)
        click_to_open.click()

        # everything is relative to this though
        datepicker = obj.driver.find_element_by_id('ui-datepicker-div')

        # is current year?
        year_element = datepicker.find_element_by_css_selector('.ui-datepicker-year')
        current_year = year_element.text
        year_difference = int(current_year) - val['year']
        _how_many_clicks += year_difference * 12
        
        # is current month?
        month_element = datepicker.find_element_by_css_selector('.ui-datepicker-month')
        current_month = month_element.text
        months = ['January', 'February', 'March', 'April', 'May', 'June',
                  'July', 'August', 'September', 'October', 'November', 'December']
        current_month_number = months.index(current_month) + 1
        month_difference = current_month_number - val['month']
        _how_many_clicks += month_difference
        
        # navigate to correct month
        if _how_many_clicks != 0:
            if _how_many_clicks < 0:
                _how_many_clicks = abs(_how_many_clicks)
                month_mover_locator = '.ui-datepicker-next'
            else:
                month_mover_locator = '.ui-datepicker-prev'

            for x in range(0, _how_many_clicks):
                month_mover = datepicker.find_element_by_css_selector(month_mover_locator)
                month_mover.click()
        
        has_date = datepicker.find_elements_by_xpath('//table//a[text()="%s"]' % val['day'])
        if len(has_date) == 1:
            has_date[0].click()
        else:
            raise NoSuchDayException()

    def __get__(self, obj, cls=None):
        locator_type = locator[:locator.find("=")]
        if locator_type not in ['css', 'id']:
            raise saunter.exceptions.InvalidLocatorString(locator)

        locator_value = locator[locator.find("=") + 1:]
        if locator_type == 'css':
            _locator = locator_value
        elif locator_type == 'id':
            _locator = '#%s' % locator_value

        current_date = obj.driver.execute_script('return $(arguments[0]).datepicker("getDate");', _locator)
        return current_date
