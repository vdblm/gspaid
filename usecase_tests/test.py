import time
import unittest

from selenium import webdriver


class ContactAdminTest(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome('C:\\Users\\vahid\\Desktop\\chromedriver.exe')

    def test_contact_admin(self):
        driver = self.driver
        driver.get("file:///D:/Sharif/Term/SAD/gspaid/documents/design/wireframe/general/home.html")
        time.sleep(1)
        name = driver.find_element_by_id("name")
        email = driver.find_element_by_id("email")
        description = driver.find_element_by_id("description")
        
