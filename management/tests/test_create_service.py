from django.contrib.auth.models import User
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
        euro = Currency.objects.create(
            name="IRR"
        )
        self.request_type = RequestType.objects.create(
            currency=euro,
            amount=123456,
            information="You wanna buy it anyway"
        )

    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=True)
    def help_create_service(self, currency_name, amount, information):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        self.assertTrue("Dashboard" in self.web_driver.page_source)
        self.open('/management/add_request_type')
        title_element = self.web_driver.find_element_by_id('title')
        amount_element = self.web_driver.find_element_by_id('amount')
        currency_element = self.web_driver.find_element_by_id('currency')
        extra_info_element = self.web_driver.find_element_by_id('extra-info')

        title_element.send_keys('toefl')
        amount_element.send_keys('10000')
        currency_element.send_keys('EUR')
        extra_info_element.send_keys('My fathers name is Saljough')

        extra_info_element.submit()

        self.assertTrue('Created request type successfully' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_create_service_new_service(self):
        self.help_create_service("IRR", 98765, "Not good, do not use it")


