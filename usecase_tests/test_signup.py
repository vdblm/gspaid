import time
import unittest

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class ContactAdminTest(unittest.TestCase):
    def setUp(self):
        self.browser = webdriver.Firefox()
        self.wireframe_host_name = "file:///home/alto/Documents/SAD/gspaid/documents/design/wireframe"

    def wireframe_address(self, path):
        return self.wireframe_host_name + path

    def test_signup_basic_scenario(self):
        browser = self.browser

        browser.get(self.wireframe_address('/customer/signup_login.html'))

        first_name_input = browser.find_element_by_id('firstName')
        last_name_input = browser.find_element_by_id('lastName')
        username_input = browser.find_element_by_id('username')
        phone_number_input = browser.find_element_by_id('phoneNumber')
        password_input = browser.find_element_by_id('password')
        password_confirmation_input = browser.find_element_by_id('passwordConfirmation')
        email_input = browser.find_element_by_id('email')

        first_name_input.send_keys('Ali')
        last_name_input.send_keys('Asgari')
        username_input.send_keys('alto')
        phone_number_input.send_keys('09136466666')
        password_input.send_keys('very_easy_password')
        password_confirmation_input.send_keys('very_easy_password')
        email_input.send_keys('altostratous@god.com')
        submit_button.click()

        self.assertTrue('Successfully' in browser.page_source)

    def tearDown(self):
        super().tearDown()
        self.browser.close()


