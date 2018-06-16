from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def test_live_currency(self):
        self.open("/financial/live_currency")
        self.assertTrue('Live Currency' in self.web_driver.page_source)
