from django.conf import settings
from django.db import models

from financial.models import Currency
from financial.models import Transaction


# Fee Transaction should be in all requests (some requests like "Toefl" and "Uni Apply" don't need it).
# Fee is not handled yet. (in Transaction to_amount = from_amount - fee)
# Ceiling and Floor is not handled yet.

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

    def create_transaction(self):
        self.transaction = Transaction.objects.create(from_currency=self.request_type.src_currency,
                                                      to_currency=self.request_type.dst_currency,
                                                      from_amount=self.amount,
                                                      to_amount=self.amount,
                                                      from_user=self.user,
                                                      to_user=self.user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.create_transaction()
        self.transaction.save()
        super().save(force_insert, force_update, using, update_fields)


# Why should it point to RequestType??
# The only thing differs between different currencies is fee law
# which we consider the same here (AnonymousRequest).
class AnonymousRequest(models.Model):
    src_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="going_anonymousRequest_set")
    dst_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="coming_anonymousRequest_set")

    currency = models.ForeignKey(Currency)

    request_type = models.ForeignKey(RequestTypeBase)

    amount = models.DecimalField(max_digits=128, decimal_places=64)
    transaction = models.ForeignKey(Transaction)

    def create_transaction(self):
        self.transaction = Transaction.objects.create(from_currency=self.currency,
                                                      to_currency=self.currency,
                                                      from_amount=self.amount,
                                                      to_amount=self.amount,
                                                      from_user=self.src_user,
                                                      to_user=self.dst_user)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.create_transaction()
        self.transaction.save()
        super().save(force_insert, force_update, using, update_fields)


class RequestType(RequestTypeBase):
    currency = models.ForeignKey(Currency)
    # Set null if amount is not fixed
    amount = models.DecimalField(max_digits=128, decimal_places=64, null=True, blank=True)
    information = models.TextField()


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="userGoing_request_set")
    employee = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="employeeComing_request_set")
    request_type = models.ForeignKey(RequestType)
    transaction = models.ForeignKey(Transaction)

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
    attachment = models.FileField()

    user_description = models.TextField()
    employee_description = models.TextField()

    def create_transaction(self):
        self.transaction = Transaction.objects.create(from_currency=self.request_type.currency,
                                                      to_currency=self.request_type.currency,
                                                      from_amount=self.request_type.amount,
                                                      to_amount=self.request_type.amount,
                                                      from_user=self.user,
                                                      to_user=settings.AUTH_SUPER_USER_MODEL)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.create_transaction()
        self.transaction.save()
        super().save(force_insert, force_update, using, update_fields)

