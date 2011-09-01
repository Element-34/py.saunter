from saunter.testcase.webdriver import SaunterTestCase

from pages.shirts import ShirtPage

import pytest

class CheckLoginExample(SaunterTestCase):
    @pytest.marks('deep', 'ebay', 'shirts')
    def test_collar_style(self):
        s = ShirtPage()
        s.go_to_mens_dress_shirts()
        s.change_collar_style("Banded (Collarless)")
        assert(s.is_collar_selected("Banded (Collarless)"))
