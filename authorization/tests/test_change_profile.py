import time

from authorization.models import User
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
            phone_number="+989136496618",
            email="altostratous@gspaid.com"
        )
        self.user = User.objects.create_user(
            username="alto2",
            first_name="ali2",
            last_name="asgari2",
            password="asdfghjkl;2",
            phone_number="+989136496618",
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
        notification_element = web_driver.find_element_by_name('notification_type')
        notification_element.send_keys(notification)

        notification_element.submit()

        time.sleep(1)

    def help_edit_profile(self, first_name, last_name, email, notification, phone_number):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Profile").click()

        time.sleep(1)

        first_name_element = web_driver.find_element_by_name('first_name')
        last_name_element = web_driver.find_element_by_name('last_name')
        email_element = web_driver.find_element_by_name('email')
        phone_number_element = web_driver.find_element_by_name('phone_number')
        notification_element = web_driver.find_element_by_name('notification_type')

        first_name_element.clear()
        last_name_element.clear()
        email_element.clear()
        phone_number_element.clear()
        first_name_element.send_keys(first_name)
        last_name_element.send_keys(last_name)
        email_element.send_keys(email)
        phone_number_element.send_keys(phone_number)
        notification_element.send_keys(notification)

        notification_element.submit()

        time.sleep(1)

    @override_settings(DEBUG=True)
    def test_edit_profile_successful(self):
        self.help_edit_profile(
            first_name="ali3",
            last_name="asgari3",
            email="altostratous3@gspaid.com",
            phone_number="+989136496628",
            notification="Email"
        )

        self.assertTrue("successful" in self.web_driver.page_source)
        self.web_driver.quit()

    def help_change_password(self, old_password, new_password):
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Profile").click()

        change_password_element = web_driver.find_element_by_link_text('Change Password')
        change_password_element.click()

        time.sleep(1)

        old_password_element = web_driver.find_element_by_name('old_password')
        new_password_1_element = web_driver.find_element_by_name('new_password1')
        new_password_2_element = web_driver.find_element_by_name('new_password2')

        old_password_element.send_keys(old_password)
        new_password_1_element.send_keys(new_password)
        new_password_2_element.send_keys(new_password)

        submit_attempt = web_driver.find_element_by_xpath("//*[@type='submit']")
        if submit_attempt is None:
            raise Exception
        submit_attempt.submit()
        # self.assertTrue('Profile changed successfully' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_change_password_wrong_old(self):
        self.help_change_password("wrong-old-pass", "new-pass")
        time.sleep(1)
        self.assertTrue('Your old password was entered incorrectly.' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_change_password_successful(self):
        self.help_change_password("asdfghjkl;", "new-pass")
        time.sleep(1)
        self.assertTrue('Password change successful' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_notification_select_SMS_successful(self):
        self.help_notification_select("SMS")
        self.assertTrue('Profile saved successfully!' in self.web_driver.page_source)

    @override_settings(DEBUG=True)
    def test_notification_select_Email_successful(self):
        self.help_notification_select("Email")
        self.assertTrue('Profile saved successfully!' in self.web_driver.page_source)

