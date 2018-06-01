from __future__ import unicode_literals

from django.db import models


class Ticket(models.Model):
    name = models.TextField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False)
    message = models.TextField(null=False, blank=False)
