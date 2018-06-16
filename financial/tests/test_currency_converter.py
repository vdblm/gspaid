import re
import time

from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_converter(self):
        self.open("/financial/currency_converter")
        web_driver = self.web_driver
        time.sleep(3)
        amount_dollar_field = web_driver.find_element_by_css_selector('input[title="United States dollar"]')
        amount_euro_field = web_driver.find_element_by_css_selector('input[title="Euro"]')

        dollar = float(amount_dollar_field.get_attribute('value'))
        euro = float(amount_euro_field.get_attribute('value'))

        ratio = 310
        dollar = dollar * ratio

        amount_dollar_field.clear()
        amount_dollar_field.send_keys(str(dollar))
        new_euro = float(amount_euro_field.get_attribute('value'))

        time.sleep(1)

        self.assertAlmostEqual(ratio * euro, new_euro, places=0)

        web_driver.close()

