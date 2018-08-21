import time

from authorization.models import User
from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()

    def help_exchange_currency_not_final(self, amount_to_change, from_currency, to_currency):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Wallet").click()

        time.sleep(1)

        amount_to_change_element = web_driver.find_element_by_id('amount-to-change')
        from_currency_element = web_driver.find_element_by_id('from-currency')
        to_currency_element = web_driver.find_element_by_id('to-currency')

        amount_to_change_element.send_keys(amount_to_change)
        from_currency_element.send_keys(from_currency)
        to_currency_element.send_keys(to_currency)

    def test_exchange_currency_wrong_input(self):
        self.help_exchange_currency_not_final("sdg235", "Rial", "$")
        update_change_info = self.web_driver.find_element_by_id("update-change-info")
        update_change_info.click()
        time.sleep(1)
        self.assertTrue("input incorrect")

    def test_exchange_currency_successful(self):
        self.help_exchange_currency_not_final("10000", "Rial", "$")
        # amount_to_get_element.
        web_driver = self.web_driver
        charge = web_driver.find_element_by_id("change")
        charge.click()
        time.sleep(1)

        self.assertTrue("Changed successfully!" in self.web_driver.page_source)
