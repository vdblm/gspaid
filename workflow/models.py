from django.conf import settings
from django.db import models
from solo.models import SingletonModel

from financial.models import Currency


class RequestTypeBase(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    description = models.TextField()
    wage_rule = models.CharField(max_length=128, null=False, blank=False, default='0 0')
    # Transaction object
    # Ceiling and Floor


# Delete singleton,
class ExchangeRequestType(RequestTypeBase, SingletonModel):
    # Transaction object for fee
    # currency_source
    # currency_destination
    pass

# class ExchangeRequest points to ExchangeRequestType
    # Constructor: construct Transaction
    # amount
    # override save method: save
    # user

# class AnonymousRequest points to RequestTypeBase and Currency
    # user_source
    # user_dest
    # Transaction function
    # override save method.


class RequestType(RequestTypeBase):
    currency = models.ForeignKey(Currency)
    # Set null if amount is not fixed
    amount = models.DecimalField(max_digits=128, decimal_places=64)
    information = models.TextField()


class Request(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL)
    #employee
    request_type = models.ForeignKey(RequestType)

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

    # Add function to change status and financial Transaction
    # override save method: save
