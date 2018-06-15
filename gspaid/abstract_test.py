from django.test import LiveServerTestCase
from selenium import webdriver


class SeleniumTestCase(LiveServerTestCase):
    """
    A base test case for Selenium, providing hepler methods for generating
    clients and logging in profiles.
    """
    def setUp(self):
        self.wd = webdriver.Chrome()
        super(SeleniumTestCase, self).setUp()

    def tearDown(self):
        self.wd.quit()
        super(SeleniumTestCase, self).tearDown()

    def open(self, url):
        self.wd.get("%s%s" % (self.live_server_url, url))