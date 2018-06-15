from django.contrib.auth.models import User
from django.db import models

from financial.models import Currency


class RequestType(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    currency = models.ForeignKey(Currency)
    description = models.TextField()
    amount = models.DecimalField(max_digits=128, decimal_places=64)
    extra_information = models.TextField()


class Request(models.Model):
    user = models.ForeignKey(User)
    request_type = models.ForeignKey(RequestType)

    CREATED = 'created'
    IN_PROGRESS = 'in_progress'
    FAILED = 'assigned'
    SUCCEEDED = 'succeeded'

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (IN_PROGRESS, 'In progress'),
        (FAILED, 'Failed'),
        (SUCCEEDED, 'Succeeded'),
    )

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=CREATED)
    attachment = models.FileField()

    user_description = models.TextField()
    employee_description = models.TextField()
