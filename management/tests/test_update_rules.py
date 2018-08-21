from authorization.models import User
import re
import time

from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from financial.models import Currency
from gspaid.abstract_test import SeleniumTestCase
from workflow.models import RequestType


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.super_user = User.objects.create_superuser(
            username="alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=True)
    def help_create_service(self, max_transaction_per_day, min_transaction_per_day):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Settings").click()

        max_transaction= web_driver.find_element_by_id('max_transaction_per_day')
        min_transaction = web_driver.find_element_by_id('min_transaction_per_day')

        max_transaction.send_keys(max_transaction_per_day)
        min_transaction.send_keys(min_transaction_per_day)
        min_transaction.submit()

    @override_settings(DEBUG=True)
    def test_create_service_new_service_successful(self):
        self.help_create_service(max_transaction_per_day=1000, min_transaction_per_day=50)
        self.assertTrue('Settings Changed Successfully!' in self.web_driver.page_source)
