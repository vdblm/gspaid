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
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Create New Request Type").click()

        title_element = web_driver.find_element_by_id('title')
        amount_element = web_driver.find_element_by_id('amount')
        currency_element = web_driver.find_element_by_id('currency')
        extra_info_element = web_driver.find_element_by_id('extra-info')

        title_element.send_keys('toefl')
        amount_element.send_keys('10000')
        currency_element.send_keys('EUR')
        extra_info_element.send_keys('My fathers name is Saljough')

        extra_info_element.submit()

    @override_settings(DEBUG=True)
    def test_create_service_new_service_successful(self):
        self.help_create_service("IRR", 98765, "It is newwwww")
        self.assertTrue('Created request type successfully' in self.web_driver.page_source)
        notification_link = self.web_driver.find_element_by_link_text('Send Notification')
        notification_link.click()
        self.assertTrue('Notification' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_create_service_new_service_duplicate_name(self):
        self.help_create_service(
            "IRR",
            amount=123456,
            information="You wanna buy it anyway"
        )
        self.assertTrue('duplicate' in self.web_driver.page_source)


