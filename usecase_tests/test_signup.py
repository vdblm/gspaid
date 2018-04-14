import unittest

from selenium import webdriver


class ContactAdminTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.wireframe_host_name = "file:///home/alto/Documents/SAD/gspaid/documents/design/wireframe"

    def wireframe_address(self, path):
        return self.wireframe_host_name + path

    def base_signup(self, first_name, last_name, username, phone_number, password, password_confirmation, email):
        browser = self.browser

        browser.get(self.wireframe_address('/customer/signup_login.html'))

        first_name_input = browser.find_element_by_id('firstName')
        last_name_input = browser.find_element_by_id('lastName')
        username_input = browser.find_element_by_id('username')
        phone_number_input = browser.find_element_by_id('phoneNumber')
        password_input = browser.find_element_by_id('password')
        password_confirmation_input = browser.find_element_by_id('passwordConfirmation')
        email_input = browser.find_element_by_id('email')
        submit_button = browser.find_element_by_css_selector('input[type=submit]')

        first_name_input.send_keys(first_name)
        last_name_input.send_keys(last_name)
        username_input.send_keys(username)
        phone_number_input.send_keys(phone_number)
        password_input.send_keys(password)
        password_confirmation_input.send_keys(password_confirmation)
        email_input.send_keys(email)
        submit_button.submit()

    def test_signup_basic_scenario(self):
        self.base_signup('Ali', 'Asgari', 'alto', '09136466666',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')

        self.assertTrue('YOUR ACCOUNT HAS BEEN CREATED' in self.browser.page_source)

    def test_signup_alternative_incomplete_data_scenario(self):
        self.base_signup('Ali', 'Asgari', 'alto', '',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')

        self.assertTrue('Incomplete data' in self.browser.page_source)

    def test_signup_alternative_incorrect_input_format_scenario(self):
        self.base_signup('Ali', 'Asgari', 'alto', '',
                         'short', 'short', 'altostratous.god.com')

        labels = self.browser.find_elements_by_css_selector("label")

        password_error_seen = False
        email_error_seen = False

        for label in labels:
            if 'Password must be at least 8 characters long.' in label.text:
                password_error_seen = True

            if 'Wrong Email Format.' in label.text:
                email_error_seen = True

        self.assertTrue(password_error_seen)
        self.assertTrue(email_error_seen)

    def test_signup_alternative_passwords_unmatched_scenario(self):
        self.base_signup('Ali', 'Asgari', 'alto', '09136466666',
                         'a_password', 'another_password', 'altostratous@god.com')

        self.assertTrue("Passwords don't match" in self.browser.page_source)

    def test_signup_alternative_username_taken_scenario(self):
        self.base_signup('Ali', 'Asgari', 'alto', '09136466666',
                         'very_easy_password', 'very_easy_password', 'altostratous@god.com')

        self.base_signup('Ali2', 'Asgari2', 'alto', '09136466636',
                         'another_easy_password', 'another_easy_password', 'altosous@god.com')

        self.assertTrue("Username is taken" in self.browser.page_source)

    def tearDown(self):
        super().tearDown()
        self.browser.close()
