import re
import time
import unittest

from selenium import webdriver


class ContactAdminTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:\\Users\\vahid\\Desktop\\chromedriver.exe')

    def help_test_contact_admin(self, name, email, description):
        driver = self.driver
        driver.get("file:///D:/Sharif/Term/SAD/gspaid/documents/design/wireframe/general/home.html")
        time.sleep(1)
        name_field = driver.find_element_by_id("name")
        email_field = driver.find_element_by_id("email")
        description_field = driver.find_element_by_id("description")

        self.assertIsNotNone(name_field)
        self.assertIsNotNone(email_field)
        self.assertIsNotNone(description_field)

        name_field.send_keys(name)
        email_field.send_keys(email)
        description_field.send_keys(description)

        submit_attempt = driver.find_element_by_xpath("//*[@type='submit']")
        self.assertIsNotNone(submit_attempt)

        submit_attempt.submit()

        email_pattern = "[^@]+@[^@]+\.[^@]+"
        if (not re.match(email_pattern, email)) or len(name) is 0 or len(description) is 0:
            self.assertIn("Wrong Email or Empty Field", driver.page_source)
        driver.close()

    def test_contact_admin_wrong_email(self):
        self.help_test_contact_admin(email="vahid.mail.com", name="vahid", description="hello")

    def test_contact_admin_empty_name(self):
        self.help_test_contact_admin(email="vahid@gmail.com", name="", description="hello")

    def test_contact_admin_empty_description(self):
        self.help_test_contact_admin(email="vahid@gmail.com", name="vahid", description="")

    def test_contact_admin_base_scenario(self):
        self.help_test_contact_admin(email="vahid@gmail.com", name="vahid", description="hello")


unittest.main()
