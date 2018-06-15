from django.contrib.auth.models import User
import re
import time

from django.test import override_settings

from gspaid.abstract_test import SeleniumTestCase


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

    @staticmethod
    def help_login(selenium_test_case, username, password):
        selenium_test_case.open("/authorization/login")
        time.sleep(1)

        wd = selenium_test_case.wd

        username_field = wd.find_element_by_name("username")
        password_field = wd.find_element_by_name("password")

        username_field.send_keys(username)
        password_field.send_keys(password)

        submit_attempt = wd.find_element_by_xpath("//*[@type='submit']")
        if submit_attempt is None:
            raise Exception

        submit_attempt.submit()
        time.sleep(1)

    @override_settings(DEBUG=True)
    def test_login_successful(self):
        wd = self.wd
        self.help_login(self, username="alto", password="asdfghjkl;")

        self.assertTrue("Dashboard" in self.wd.page_source)

    @override_settings(DEBUG=True)
    def test_login_wrong_username_password(self):
        wd = self.wd
        self.help_login(self, username="amin", password="qwertyuiop[]")

        self.assertTrue("Please enter a correct username and password" in self.wd.page_source)
