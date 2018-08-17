import time
from django.contrib.auth.models import User
from django.test import override_settings

from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.employee = User.objects.create_user(
            username='employee',
            password='employee',
            email='employee@gspaid.ir',
            is_staff=True
        )

    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=True)
    def employee_login(self):
        self.open('/authorization/login')
        username_element = self.web_driver.find_element_by_name('username')
        password_element = self.web_driver.find_element_by_name('password')

        username_element.send_keys('employee')
        password_element.send_keys('employee')

        password_element.submit()
        time.sleep(1)
        self.assertTrue('Requests' in self.web_driver.page_source)

    def employee_select_new_request(self):
        new_request_link = self.web_driver.find_element_by_link_text('Check New Request')
        new_request_link.click()
        time.sleep(1)

        # to assert if the cost is shown
        self.web_driver.find_element_by_id('cost')

    def change_status(self, status):
        status_element = self.web_driver.find_element_by_name('status')
        status_element.send_keys(status)
        status_element.submit()
        time.sleep(1)

    def test_employee_check_correct_request_without_notification(self):
        self.employee_login()
        self.employee_select_new_request()

        # change status to In Progress
        self.change_status('In Progress')

        # assert if Notification link is shown
        self.assertTrue('Notification' in self.web_driver.page_source)

    def test_employee_check_correct_request_with_notification(self):
        self.test_employee_check_correct_request_without_notification()

        notification_text_element = self.web_driver.find_element_by_id('notification_text')
        notification_text_element.send_keys('Your request has been approved')
        notification_text_element.submit()

        self.assertTrue('Notification sent' in self.web_driver.page_source)

    def test_employee_check_wrong_request_without_notification(self):
        self.employee_login()
        self.employee_select_new_request()

        # change status to In Progress
        self.change_status('Failed')

        # assert if Notification link is shown
        self.assertTrue('Notification' in self.web_driver.page_source)

    def test_employee_check_wrong_request_with_notification(self):
        self.test_employee_check_wrong_request_without_notification()

        notification_text_element = self.web_driver.find_element_by_id('notification_text')
        notification_text_element.send_keys("You didn't provided us with you father's name")
        notification_text_element.submit()

        self.assertTrue('Notification sent' in self.web_driver.page_source)

    def test_employee_check_suspicious_request_without_notification(self):
        self.employee_login()
        self.employee_select_new_request()

        # change status to In Progress
        self.change_status('Suspicious')

        # assert if Notification link is shown
        self.assertTrue('Notification' in self.web_driver.page_source)

    def test_employee_check_suspicious_request_with_notification(self):
        self.test_employee_check_suspicious_request_without_notification()

        notification_text_element = self.web_driver.find_element_by_id('notification_text')
        notification_text_element.send_keys("You didn't provided us with you father's name")
        notification_text_element.submit()

        self.assertTrue('Notification sent' in self.web_driver.page_source)
