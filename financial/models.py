from __future__ import unicode_literals

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
