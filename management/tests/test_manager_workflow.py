from django.contrib.auth.models import User
import re
import time

from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from financial.models import Currency
from gspaid.abstract_test import SeleniumTestCase
from workflow.models import RequestType, Request


class ManagerWorkFlowTests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.super_user = User.objects.create_superuser(
            username="alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )
        self.customer_user = User.objects.create_user(
            username="customer_alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )
        self.employee_user = User.objects.create_user(
            username="employee_alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )
        self.IRR = Currency.objects.create(
            name="IRR"
        )

        self.EUR = Currency.objects.create(
            name="EUR"
        )
        self.request_type = RequestType.objects.create(
            name="duplicate_name",
            description="go hell",
            currency=self.EUR,
            amount=123456,
            information="father's name = ?"
        )
        Request.objects.create(
            user=self.customer_user,
            request_type=self.request_type,
            status=Request.CREATED,
        )


    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=True)
    def help_create_service(self, title, currency_name, amount, extra_info):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Create New Request Type").click()

        title_element = web_driver.find_element_by_id('title')
        amount_element = web_driver.find_element_by_id('amount')
        currency_element = web_driver.find_element_by_id('currency')
        extra_info_element = web_driver.find_element_by_id('extra-info')

        title_element.send_keys(title)
        amount_element.send_keys(amount)
        currency_element.send_keys(currency_name)
        extra_info_element.send_keys(extra_info)

        extra_info_element.submit()

    @override_settings(DEBUG=True)
    def test_create_service_new_service_successful(self):
        self.help_create_service("IRR", 98765, "It is newwwww", "Father's name: ......")
        self.assertTrue('Created request type successfully' in self.web_driver.page_source)
        notification_link = self.web_driver.find_element_by_link_text('Send Notification')
        notification_link.click()
        self.assertTrue('Notification' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_create_service_new_service_duplicate_name(self):
        self.help_create_service(
            title="duplicate_name",
            currency_name="IRR",
            amount=123456,
            extra_info="You wanna buy it anyway",
        )
        self.assertTrue('duplicate' in self.web_driver.page_source)

    def test_send_notification(self):
        self.test_create_service_new_service_successful()

        notification_text_element = self.web_driver.find_element_by_id('notification_text')
        notification_text_element.send_keys('This is a new service we are adding.')
        notification_text_element.submit()

        self.assertTrue('Notification sent' in self.web_driver.page_source)

    def test_view_all_requests(self):
        # login the admin user
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")

        requests_page_link = self.web_driver.find_element_by_link_text("Requests")

        requests_page_link.click()

        self.assertTrue('Requests' in self.web_driver.page_source, msg='The recently added request is not shown in '
                                                                       'the requests page for the admin')

        # we created a request for the customer user on setup.
        # assert that his or her name is shown in the requests page
        self.assertTrue(self.customer_user.username in self.web_driver.page_source)

        self.web_driver.find_element_by_link_text('Details').click()

        self.web_driver.find_element_by_id('status')
        self.web_driver.find_element_by_id('costumer')
        self.web_driver.find_element_by_id('employee')
        self.web_driver.find_element_by_id('amount')
        self.web_driver.find_element_by_id('title')
        self.web_driver.find_element_by_id('extra-info')
        self.web_driver.find_element_by_id('extra-data')
        self.web_driver.find_element_by_link_text('Zipped files')

    def test_view_all_users(self):
        # login the admin user
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")

        requests_page_link = self.web_driver.find_element_by_link_text("Users")

        requests_page_link.click()

        # self.assertTrue('Users' in self.web_driver.page_source, msg='The recently added user is not shown in '
        #                                                             'the users page for the admin')

        # we created a request for the customer user on setup.
        # assert that his or her name is shown in the requests page
        self.assertTrue(self.customer_user.username in self.web_driver.page_source)

        self.web_driver.find_element_by_link_text('Details').click()

        self.web_driver.find_element_by_id('first_name')
        self.web_driver.find_element_by_id('last_name')
        self.web_driver.find_element_by_id('type')
        self.web_driver.find_element_by_id('salary')
        self.web_driver.find_element_by_id('username')
        self.web_driver.find_element_by_id('phone_number')
        self.web_driver.find_element_by_id('email')
