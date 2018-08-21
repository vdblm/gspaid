import time
from authorization.models import User
from django.test import override_settings

from gspaid.abstract_test import SeleniumTestCase

from authorization.tests.test_login import Tests as Authorization_Test
from financial.tests.test_charge_wallet import Tests as Financial_Test


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.user = User.objects.create_user(
            username="vdblm",
            first_name="vahid",
            last_name="balazadeh",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

    def tearDown(self):
        super().tearDown()
    
    @override_settings(DEBUG=True)
    def help_send_request(self, title, extra_data):
        Authorization_Test.help_login(self, username="vdblm", password="asdfghjkl;")

        new_request_link = self.web_driver.find_element_by_link_text('Requests')
        new_request_link.click()
        time.sleep(1)

        web_driver = self.web_driver

        title_element = web_driver.find_element_by_id('title')
        extra_data_element = web_driver.find_element_by_id('extra-data')

        title_element.send_keys(title)
        extra_data_element.send_keys(extra_data)

        self.submit = extra_data_element.submit()

    def test_costumer_correct_request(self):
        Financial_Test.test_charge_wallet(self)

        self.help_send_request(title='TOEFL Exam', extra_data='extra_data')
        self.assertTrue('Successful' in self.web_driver.page_source)

    def test_costumer_not_enough_money(self):

        self.help_send_request(title='Pay for visa', extra_data='extra_data')
        self.assertTrue('Not enough money' in self.web_driver.page_source)
