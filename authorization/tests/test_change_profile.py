import time

from django.contrib.auth.models import User
from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )
        self.user = User.objects.create_user(
            username="alto2",
            first_name="ali2",
            last_name="asgari2",
            password="asdfghjkl;2",
            email="altostratous2@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()

    def help_notification_select(self, notification):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Profile").click()

        time.sleep(1)
        notification_element = web_driver.find_element_by_id('notification')
        notification_element.send_keys(notification)

        notification_element.submit()

        time.sleep(1)

    def help_edit_profile(self, first_name, last_name, email, notification, extra_info):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Profile").click()

        time.sleep(1)

        first_name_element = web_driver.find_element_by_id('firstName')
        last_name_element = web_driver.find_element_by_id('lastName')
        email_element = web_driver.find_element_by_id('email')
        extra_info_element = web_driver.find_element_by_id('other')

        notification_element = web_driver.find_element_by_id('notification')

        first_name_element.clear()
        last_name_element.clear()
        email_element.clear()
        extra_info_element.clear()
        first_name_element.send_keys(first_name)
        last_name_element.send_keys(last_name)
        email_element.send_keys(email)
        extra_info_element.send_keys(extra_info)
        notification_element.send_keys(notification)

        change_password_element = web_driver.find_element_by_id("change-profile")
        change_password_element.click()

        time.sleep(1)

    @override_settings(DEBUG=True)
    def test_edit_profile_successful(self):
        self.help_edit_profile(
            first_name="ali3",
            last_name="asgari3",
            email="altostratous3@gspaid.com",
            extra_info="this is new",
            notification="Email"
        )

        self.assertTrue("successful" in self.web_driver.page_source)
        self.web_driver.quit()

    def help_change_password(self, old_password, new_password):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Profile").click()

        change_password_element = web_driver.find_element_by_id("change-password")
        change_password_element.click()

        time.sleep(1)

        old_password_element = web_driver.find_element_by_id('oldpassword')
        new_password_element = web_driver.find_element_by_id('newpassword')

        old_password_element.send_keys(old_password)
        new_password_element.send_keys(new_password)

        submit_attempt = web_driver.find_element_by_xpath("//*[@type='submit']")
        if submit_attempt is None:
            raise Exception
        submit_attempt.submit()
        # self.assertTrue('Profile changed successfully' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_change_password_wrong_old(self):
        self.help_change_password("wrong-old-pass", "new-pass")
        self.assertTrue('password is wrong' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_change_password_successful(self):
        self.help_change_password("asdfghjkl;", "new-pass")
        self.assertTrue('CHANGED' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_notification_select_SMS_successful(self):
        self.help_notification_select("SMS")
        self.assertTrue('CHANGED' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_notification_select_Email_successful(self):
        self.help_notification_select("Email")
        self.assertTrue('CHANGED' in self.web_driver.page_source)

