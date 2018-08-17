from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_about_us(self):
        self.open("/misc/about_us")
        self.assertTrue('About Us' in self.web_driver.page_source)

    def test_rules(self):
        self.open("/misc/rules")
        self.assertTrue('Rules' in self.web_driver.page_source)
