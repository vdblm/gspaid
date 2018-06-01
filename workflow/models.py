from django.db import models

from financial.models import Currency


class RequestType(models.Model):
    name = models.CharField(max_length=128, null=False, blank=False)
    currency = models.ForeignKey(Currency)
    description = models.TextField()
    amount = models.DecimalField()
    extra_information = models.TextField()
