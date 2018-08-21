import time

from gspaid.abstract_test import SeleniumTestCase


class Test(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def help_signup(self, first_name, last_name, username, phone_number, password, password_confirmation, email):

        self.open('/authorization/register')
        time.sleep(1)

        web_driver = self.web_driver

        first_name_input = web_driver.find_element_by_name('first_name')
        last_name_input = web_driver.find_element_by_name('last_name')
        username_input = web_driver.find_element_by_name('username')
        phone_number_input = web_driver.find_element_by_name('phone_number')
        password_input = web_driver.find_element_by_name('password1')
        password_confirmation_input = web_driver.find_element_by_name('password2')
        email_input = web_driver.find_element_by_name('email')

        first_name_input.send_keys(first_name)
        last_name_input.send_keys(last_name)
        username_input.send_keys(username)
        phone_number_input.send_keys(phone_number)
        password_input.send_keys(password)
        password_confirmation_input.send_keys(password_confirmation)
        email_input.send_keys(email)
        username_input.submit()

    def test_signup_basic_scenario(self):
        username = 'alto'
        self.help_signup('Ali', 'Asgari', username, '09136466666',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')
        time.sleep(1)
        self.assertTrue(username in self.web_driver.page_source)

    def test_signup_alternative_incomplete_data_scenario(self):
        self.help_signup('Ali', 'Asgari', 'alto', '',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')
        time.sleep(1)
        self.assertTrue('This field is required' in self.web_driver.page_source)

    def test_signup_alternative_incorrect_input_format_scenario(self):
        self.help_signup('Ali', 'Asgari', 'alto', '+989136496618',
                         'short', 'short', 'altostratous.god.com')
        time.sleep(1)
        self.assertTrue('password is too short' in self.web_driver.page_source)
        self.assertTrue('Enter a valid email address' in self.web_driver.page_source)

    def test_signup_alternative_passwords_unmatched_scenario(self):
        self.help_signup('Ali', 'Asgari', 'alto', '+989136496618',
                         'a_password', 'another_password', 'altostratous@god.com')
        time.sleep(1)
        self.assertTrue("The two password fields didn't match." in self.web_driver.page_source)

    def test_signup_alternative_username_taken_scenario(self):
        self.help_signup('Ali', 'Asgari', 'alto', '09136466666',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')
        self.help_signup('Ali2', 'Asgari2', 'alto', '09136466636',
                         'another_easy_password', 'another_easy_password', 'altosous@god.com')
        time.sleep(1)
        self.assertTrue("username already exists" in self.web_driver.page_source)

    def tearDown(self):
        super().tearDown()
