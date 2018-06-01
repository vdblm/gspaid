from django.test import LiveServerTestCase
from selenium import webdriver


class LiveCurrencyTest(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(LiveCurrencyTest, self).setUp()

    def test_live_currency(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/financial/live_currency')

        self.assertTrue('Live Currency' in self.selenium.page_source)

    def tearDown(self):
        self.selenium.quit()
        super(LiveCurrencyTest, self).tearDown()
