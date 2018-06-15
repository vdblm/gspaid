from django.contrib.auth.models import User
import re
import time

from django.test import override_settings

from authorization.tests.test_login import Tests as AuthorizationTests
from financial.models import Currency
from gspaid.abstract_test import SeleniumTestCase
from workflow.models import RequestType


class Tests(SeleniumTestCase):
    def setUp(self):
        super().setUp()
        self.super_user = User.objects.create_superuser(
            username="alto",
            first_name="ali",
            last_name="asgari",
            password="asdfghjkl;",
            email="altostratous@gspaid.com"
        )
        euro = Currency.objects.create(
            name="IRR"
        )
        self.request_type = RequestType.objects.create(
            currency=euro,
            amount=123456,
            information="You wanna buy it anyway"
        )

    def tearDown(self):
        super().tearDown()

    @override_settings(DEBUG=True)
    def help_create_service(self, currency_name, amount, information):
        wd = self.wd
        AuthorizationTests.help_login(self, username="alto", password="asdfghjkl;")

    @override_settings(DEBUG=True)
    def test_create_service_new_service(self):
        self.help_create_service("IRR", 98765, "Not good, do not use it")
        wd = self.wd

        self.assertTrue("Dashboard" in self.wd.page_source)
