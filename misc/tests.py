import unittest

from django.test import TestCase, LiveServerTestCase
from selenium import webdriver
from django.conf import settings

# Create your tests here.


class AboutUsTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(AboutUsTest, self).setUp()
        # self.wireframe_host_name = "/media/smakh/Study/Studing/University/6/Analyze/gspaid/misc/templates/misc"
    #
    # def wireframe_address(self, path):
    #     self.wireframe_host_name + path

    def test_about_us(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/misc/about_us')

        self.assertTrue('About Us' in self.selenium.page_source)

    def tearDown(self):
        self.selenium.quit()
        super(AboutUsTest, self).tearDown()
