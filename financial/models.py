from __future__ import unicode_literals

from django.conf import settings
from django.db import models
import requests
import json


class Currency(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False, unique=True)

    @property
    def ratio(self):
        conversion_key = 'IRR_' + self.name
        response = requests.request(
            'GET',
            'https://free.currencyconverterapi.com/api/v5/convert?q=%s&compact=ultra' % conversion_key
        )
        return float(json.load(response.text)[conversion_key])

    def __str__(self):
        return self.name


class Transaction(models.Model):
    from_currency = models.ForeignKey(Currency, related_name='going_transaction_set')
    to_currency = models.ForeignKey(Currency, related_name='coming_transaction_set')

    from_amount = models.DecimalField(max_digits=128, decimal_places=64)

    to_amount = models.DecimalField(max_digits=128, decimal_places=64)

    CREATED = 'created'
    FAILED = 'failed'
    SUCCEEDED = 'succeeded'

    STATUS_CHOICES = (
        (CREATED, 'Created'),
        (FAILED, 'Failed'),
        (SUCCEEDED, 'Succeeded'),
    )

    status = models.CharField(max_length=32, choices=STATUS_CHOICES, default=CREATED)

    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="going_transaction_set", null=True)
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="coming_transaction_set", null=True)
