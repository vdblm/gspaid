import re
import time

from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()
    #
    # def help_contact_admin(self, amount, source_currency, destination_currency):
    #     self.open("/financial/currency_converter")
    #     wd = self.wd
    #     time.sleep(1)
    #     amount_field = wd.find_element_by_name("amount")
    #     source_currency_field = wd.find_element_by_name("source currency")
    #     destination_currency_field = wd.find_element_by_name("destination_currency")
    #
    #     amount_field.send_keys(amount)
    #     source_currency_field.send_keys(source_currency)
    #     destination_currency_field.send_keys(destination_currency)
    #
    #     time.sleep(1)
    #
    #     number_pattern = "[0-9]+"
    #
    #     if not re.match(number_pattern, amount):
    #         self.assertIn("Enter a valid email", wd.page_source)
    #     elif len(name) == 0:
    #         self.assertIn("This field is required", wd.page_source)
    #     elif len(description) == 0:
    #         self.assertIn("This field is required", wd.page_source)
    #     else:
    #         self.assertIn("Sent message to admin.", wd.page_source)
    #     wd.close()
    #
    # def test_contact_admin_wrong_email(self):
    #     self.help_contact_admin(email="vahid.mail.com", name="vahid", description="hello")
    #
    # def test_contact_admin_empty_name(self):
    #     self.help_contact_admin(email="vahid@gmail.com", name="", description="hello")
    #
    # def test_contact_admin_empty_description(self):
    #     self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="")
    #
    # def test_contact_admin_base_scenario(self):
    #     self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="hello")
