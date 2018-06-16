import time
from django.contrib.auth.models import User
from django.test import override_settings

from gspaid.abstract_test import SeleniumTestCase


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
    def costumer_login(self):
        self.open('/authorization/login')
        username_element = self.web_driver.find_element_by_name('username')
        password_element = self.web_driver.find_element_by_name('password')

        username_element.send_keys('vdblm')
        password_element.send_keys('asdfghjkl')

        password_element.submit()
        time.sleep(1)
        self.assertTrue('Requests' in self.web_driver.page_source)

    def costumer_select_new_request(self):
        new_request_link = self.web_driver.find_element_by_link_text('Requests')
        new_request_link.click()
        time.sleep(1)
    
    @override_settings(DEBUG=True)
    def help_send_request(self, title, extra_data):
        web_driver = self.web_driver

        title_element = web_driver.find_element_by_id('title')
        extra_data_element = web_driver.find_element_by_id('extra-data')

        title_element.send_keys(title)
        extra_data_element.send_keys(extra_data)

        self.submit = extra_data_element.submit()

    def test_costumer_correct_request(self):
        self.costumer_login()
        self.costumer_select_new_request()

        self.help_send_request(title='TOEFL Exam', extra_data='extra_data')
        self.assertTrue('Successful' in self.web_driver.page_source)

    def test_costumer_not_enough_money(self):
        self.costumer_login()
        self.costumer_select_new_request()

        self.help_send_request(title='Pay for visa', extra_data='extra_data')
        self.assertTrue('Not enough money' in self.web_driver.page_source)
