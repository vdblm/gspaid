from __future__ import unicode_literals

from django.db import models


class Currency(models.Model):
    name = models.CharField(max_length=128, blank=False, null=False)
    ratio = models.IntegerField(null=False, blank=False)
