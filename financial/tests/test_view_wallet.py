import re
import time

from django.contrib.auth.models import User

from gspaid.abstract_test import SeleniumTestCase

from authorization.tests.test_login import Tests as AuthorizationTests


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        User.objects.create_user(
            username='customer',
            password='customer_password',
            email='customer@gspaid.ir',
        )

    def tearDown(self):
        super().tearDown()

    def test_converter(self):
        AuthorizationTests.help_login(self, 'customer', 'customer_password')

        wallet_link_element = self.web_driver.find_element_by_link_text('Wallet')
        wallet_link_element.click()
        time.sleep(1)

        self.web_driver.find_element_by_id('Doller')
        self.web_driver.find_element_by_id('Euro')
        self.web_driver.find_element_by_id('Rial')
