import time
from django.contrib.auth.models import User
from django.test import override_settings

from gspaid.abstract_test import SeleniumTestCase

from authorization.tests.test_login import Tests as t


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="vdblm",
            first_name="vahid",
            last_name="balazadeh",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()

    @staticmethod
    def help_send_request(selenium_test_case, amount):
        t.help_login(selenium_test_case, username="vdblm", password="asdfghjkl;")

        new_request_link = selenium_test_case.web_driver.find_element_by_link_text('Wallet')
        new_request_link.click()
        time.sleep(1)

        web_driver = selenium_test_case.web_driver

        amount_element = web_driver.find_element_by_id('amount')

        amount_element.send_keys(amount)

        selenium_test_case.submit = amount_element.submit()

    def test_charge_wallet(self):
        Tests.help_send_request(self, amount=10000000)
        self.assertTrue('Account got charged successfully!' in self.web_driver.page_source)
