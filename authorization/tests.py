from gspaid.abstract_test import SeleniumTestCase


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    # def test_about_us(self):
    #     self.open("/misc/about_us")
    #     self.assertTrue('About Us' in self.wd.page_source)
