from authorization.models import User
import re
import time

from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from financial.models import Currency, Transaction
from gspaid.abstract_test import SeleniumTestCase
from workflow.models import RequestType, Request


class ManagerWorkFlowTests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.customer_user = User.objects.create_user(
            username="customer_alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=False)
    def test_view_customer_history(self):
        # login the user
        AuthorizationTests.help_login(self, username="customer_alto", password="asdfghjkl;")

        requests_page_link = self.web_driver.find_element_by_link_text("Requests History")

        requests_page_link.click()

        self.web_driver.find_element_by_link_text('Details').click()

        self.web_driver.find_element_by_id('status')
        self.web_driver.find_element_by_id('employee')
        self.web_driver.find_element_by_id('amount')
        self.web_driver.find_element_by_id('title')
        self.web_driver.find_element_by_id('extra-info')
        self.web_driver.find_element_by_id('extra-data')
        self.web_driver.find_element_by_link_text('Zipped files')