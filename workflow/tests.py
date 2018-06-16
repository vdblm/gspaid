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
    def test_employee_login(self):
        self.open('/authorization/login')
        username_element = self.web_driver.find_element_by_name('username')
        password_element = self.web_driver.find_element_by_name('password')

        username_element.send_keys('employee')
        password_element.send_keys('employee')

        password_element.submit()

        self.assertTrue('Dashboard' in self.web_driver.page_source)

    def test_employee_check_request(self):
        self.test_employee_check_request()
