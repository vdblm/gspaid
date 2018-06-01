from django.test import LiveServerTestCase
from selenium import webdriver


class Tests(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(Tests, self).setUp()

    def tearDown(self):
        self.selenium.quit()
        super(Tests, self).tearDown()

    def test_about_us(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/financial/live_currency')
        self.assertTrue('Live Currency' in self.selenium.page_source)
