import time

from django.contrib.auth.models import User
from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from gspaid.abstract_test import SeleniumTestCase
from financial.tests.test_charge_wallet import Tests as t


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

        self.user = User.objects.create_user(
            username="shomare",
            first_name="vahid",
            last_name="bala",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )

        t.test_charge_wallet(self)

    def tearDown(self):
        super().tearDown()

    def help_transfer_internal_account(self, amount, account_number, email="", phone=""):
        AuthorizationTests.help_login(self, username="vdblm", password="asdfghjkl;")
        web_driver = self.web_driver
        self.assertTrue("Dashboard" in web_driver.page_source)
        web_driver.find_element_by_link_text("Internal Payment").click()

        time.sleep(1)

        amount_element = web_driver.find_element_by_id('amount')
        account_number_element = web_driver.find_element_by_id('account_number')
        email_element = web_driver.find_element_by_id('email')
        phone_element = web_driver.find_element_by_id('phone')

        amount_element.send_keys(amount)
        account_number_element.send_keys(account_number)
        email_element.send_keys(email)
        phone_element.send_keys(phone)
        time.sleep(1)

    def test_transfer_internal_account_wrong_input(self):
        self.help_transfer_internal_account(amount=1000, account_number="", email="you.com")
        self.assertTrue("Wrong Input!" in self.web_driver.page_source)

    def test_transfer_internal_account_wrong_saghf_kaf(self):
        self.help_transfer_internal_account(amount=0, account_number="shomare", email="altostratous@gspaid.com")
        self.assertTrue("Wrong Saghf Kaf!" in self.web_driver.page_source)

    def test_transfer_internal_account_karmozd(self):
        self.help_transfer_internal_account(amount=10000, account_number="shomare", email="altostratous@gspaid.com")
        self.assertTrue("Karmozd" in self.web_driver.page_source)

    def test_transfer_internal_account_not_enough_money(self):

        self.help_transfer_internal_account(amount=100000000, account_number="shomare", email="altostratous@gspaid.com")
        self.assertTrue("Not Enough Money" in self.web_driver.page_source)

    def test_transfer_internal_account_no_account(self):
        # TODO test database integrity
        self.help_transfer_internal_account(amount=100000000, account_number="shomarehesab nodorost ast.",
                                            email="altostratous@gspaid.com")
        self.assertTrue("There was no account with this username, We created an account and informed the owner" in
                        self.web_driver.page_source)

    def test_transfer_internal_account_correct(self):
        self.help_transfer_internal_account(amount=100000000, account_number="shomare",
                                            email="altostratous@gspaid.com")
        self.assertTrue("Transferred successfully!" in self.web_driver.page_source)
