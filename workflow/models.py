import json

import requests
from django.conf import settings
from django.db import models

from financial.models import Currency
from financial.models import Transaction
from authorization.models import SuperUser


# Fee Transaction should be in all requests (some requests like "Toefl" and "Uni Apply" don't need it).
# Fee is not handled yet. (in Transaction to_amount = from_amount - fee)
# Ceiling and Floor is not handled yet.
def calculate_balance(user, currency):
    input_transactions = Transaction.objects.filter(to_user=user).filter(to_currency=currency).filter(
        status=Transaction.SUCCEEDED)
    output_transactions = Transaction.objects.filter(from_user=user).filter(from_currency=currency).filter(
        status=Transaction.SUCCEEDED)

    input_amount = 0
    output_amount = 0
    for transaction in input_transactions:
        input_amount = input_amount + transaction.to_amount
    for transaction in output_transactions:
        output_amount = output_amount + transaction.from_amount

    return input_amount - output_amount


def check_transaction_fail(transaction):
    return transaction.from_user is not None and \
           calculate_balance(transaction.from_user,
                             transaction.from_currency) < transaction.from_amount


def ratio(first, second):
    conversion_key = str(first) + "_" + str(second)
    response = requests.request(
        'GET',
        'https://free.currencyconverterapi.com/api/v5/convert?q=%s&compact=ultra' % conversion_key
    )
    return float(json.loads(response.text)[conversion_key])


class RequestTypeBase(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField()
    wage_rule = models.CharField(max_length=128, null=False, blank=False, default='0 0')
    # Ceiling and Floor


class ExchangeRequestType(RequestTypeBase):
    # Transaction object for fee
    src_currency = models.ForeignKey(Currency, related_name="going_exchangeRequestType_set")
    dst_currency = models.ForeignKey(Currency, related_name="coming_exchangeRequestType_set")


class ExchangeRequest(models.Model):
    request_type = models.ForeignKey(ExchangeRequestType)
    amount = models.DecimalField(max_digits=128, decimal_places=64)
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    first_transaction = models.ForeignKey(Transaction, related_name="first", null=True)
    second_transaction = models.ForeignKey(Transaction, related_name="second", null=True)

    def create_transaction(self):
        site_user = SuperUser.get_solo()
        # to_amount should be calculated with ratio
        to_amount = float(self.amount) * ratio(self.request_type.src_currency.name, self.request_type.dst_currency.name)
        self.first_transaction = Transaction.objects.create(from_currency=self.request_type.src_currency,
                                                            to_currency=self.request_type.src_currency,
                                                            from_amount=self.amount,
                                                            to_amount=self.amount,
                                                            from_user=self.user,
                                                            to_user=site_user)
        self.second_transaction = Transaction.objects.create(from_currency=self.request_type.dst_currency,
                                                             to_currency=self.request_type.dst_currency,
                                                             from_amount=to_amount,
                                                             to_amount=to_amount,
                                                             from_user=site_user,
                                                             to_user=self.user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.first_transaction is None or self.second_transaction is None:
            self.create_transaction()
            if check_transaction_fail(self.first_transaction) or check_transaction_fail(self.second_transaction):
                self.first_transaction.status = Transaction.FAILED
                self.second_transaction.status = Transaction.FAILED
            else:
                self.first_transaction.status = Transaction.SUCCEEDED
                self.second_transaction.status = Transaction.SUCCEEDED
        self.first_transaction.save()
        self.second_transaction.save()
        super().save(force_insert, force_update, using, update_fields)


# Why should it point to RequestType??
# The only thing differs between different currencies is fee law
# which we consider the same here (AnonymousRequest).
class AnonymousRequest(models.Model):
    src_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="going_anonymousRequest_set")
    dst_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="coming_anonymousRequest_set")

    currency = models.ForeignKey(Currency)

    amount = models.DecimalField(max_digits=128, decimal_places=64)
    transaction = models.ForeignKey(Transaction, null=True)

    def create_transaction(self):
        self.transaction = Transaction.objects.create(from_currency=self.currency,
                                                      to_currency=self.currency,
                                                      from_amount=self.amount,
                                                      to_amount=self.amount,
                                                      from_user=self.src_user,
                                                      to_user=self.dst_user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.transaction is None:
            self.create_transaction()
            if check_transaction_fail(self.transaction):
                self.transaction.status = Transaction.FAILED
            else:
                self.transaction.status = Transaction.SUCCEEDED
        self.transaction.save()
        super().save(force_insert, force_update, using, update_fields)


class RequestType(RequestTypeBase):
    currency = models.ForeignKey(Currency)
    # Set null if amount is not fixed
    amount = models.DecimalField(max_digits=128, decimal_places=64, null=True, blank=True)
    information = models.TextField()
    is_withdraw = models.BooleanField(default=False)


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userGoing_request_set")
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="employeeComing_request_set", null=True)
    request_type = models.ForeignKey(RequestType)
    transaction = models.ForeignKey(Transaction, null=True)
    # Not sure about blank = True
    amount = models.DecimalField(max_digits=128, decimal_places=64, null=True)
    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    FAILED = 'failed'
    SUCCEEDED = 'succeeded'
    SUSPICIOUS = 'suspicious'

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (IN_PROGRESS, 'In progress'),
        (FAILED, 'Failed'),
        (SUCCEEDED, 'Succeeded'),
        (SUSPICIOUS, 'Suspicious'),
    )

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=CREATED)
    attachment = models.FileField(null=True, blank=True)

    user_description = models.TextField()
    employee_description = models.TextField(null=True)

    def create_transaction(self):
        site_user = SuperUser.get_solo()
        if self.request_type.amount is not None:
            self.amount = self.request_type.amount
        to_user = site_user
        if self.request_type.is_withdraw:
            to_user = None
        self.transaction = Transaction.objects.create(from_currency=self.request_type.currency,
                                                      to_currency=self.request_type.currency,
                                                      from_amount=self.amount,
                                                      to_amount=self.amount,
                                                      from_user=self.user,
                                                      to_user=to_user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        if self.transaction is None:
            self.create_transaction()
            if check_transaction_fail(self.transaction):
                self.transaction.status = Transaction.FAILED
            else:
                self.transaction.status = Transaction.CREATED
        self.transaction.save()
        super().save(force_insert, force_update, using, update_fields)
