import re
import time
import unittest

from django.test import LiveServerTestCase
from selenium import webdriver


class ContactAdminTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Firefox()
        self.wireframe_host_name = "http://127.0.0.1:8000"

    def wireframe_address(self, path):
        return self.wireframe_host_name + path

    def help_contact_admin(self, name, email, description):
        driver = self.selenium
        driver.get(self.wireframe_address("/management/contact_admin"))
        time.sleep(1)
        name_field = driver.find_element_by_name("name")
        email_field = driver.find_element_by_name("email")
        description_field = driver.find_element_by_name("message")

        self.assertIsNotNone(name_field)
        self.assertIsNotNone(email_field)
        self.assertIsNotNone(description_field)

        name_field.send_keys(name)
        email_field.send_keys(email)
        description_field.send_keys(description)

        submit_attempt = driver.find_element_by_xpath("//*[@type='submit']")
        self.assertIsNotNone(submit_attempt)

        submit_attempt.submit()
        time.sleep(1)

        email_pattern = "[^@]+@[^@]+\.[^@]+"

        if not re.match(email_pattern, email):
            self.assertIn("Enter a valid email", driver.page_source)
        elif len(name) == 0:
            self.assertIn("This field is required", driver.page_source)
        elif len(description) == 0:
            self.assertIn("This field is required", driver.page_source)
        else:
            self.assertIn("Sent message to admin.", driver.page_source)
        driver.close()

    def test_contact_admin_wrong_email(self):
        self.help_contact_admin(email="vahid.mail.com", name="vahid", description="hello")

    def test_contact_admin_empty_name(self):
        self.help_contact_admin(email="vahid@gmail.com", name="", description="hello")

    def test_contact_admin_empty_description(self):
        self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="")

    def test_contact_admin_base_scenario(self):
        self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="hello")

    def tearDown(self):
        super().tearDown()
        self.selenium.quit()
