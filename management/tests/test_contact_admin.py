import re
import time

from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def help_contact_admin(self, name, email, description):
        self.open("/management/contact_admin")
        wd = self.web_driver
        time.sleep(1)
        name_field = wd.find_element_by_name("name")
        email_field = wd.find_element_by_name("email")
        description_field = wd.find_element_by_name("message")

        self.assertIsNotNone(name_field)
        self.assertIsNotNone(email_field)
        self.assertIsNotNone(description_field)

        name_field.send_keys(name)
        email_field.send_keys(email)
        description_field.send_keys(description)

        submit_attempt = wd.find_element_by_xpath("//*[@type='submit']")
        self.assertIsNotNone(submit_attempt)

        submit_attempt.submit()
        time.sleep(1)

        email_pattern = "[^@]+@[^@]+\.[^@]+"

        if not re.match(email_pattern, email):
            self.assertIn("Enter a valid email", wd.page_source)
        elif len(name) == 0:
            self.assertIn("This field is required", wd.page_source)
        elif len(description) == 0:
            self.assertIn("This field is required", wd.page_source)
        else:
            self.assertIn("Sent message to admin.", wd.page_source)
        wd.close()

    def test_contact_admin_wrong_email(self):
        self.help_contact_admin(email="vahid.mail.com", name="vahid", description="hello")

    def test_contact_admin_empty_name(self):
        self.help_contact_admin(email="vahid@gmail.com", name="", description="hello")

    def test_contact_admin_empty_description(self):
        self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="")

    def test_contact_admin_base_scenario(self):
        self.help_contact_admin(email="vahid@gmail.com", name="vahid", description="hello")
