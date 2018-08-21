from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=True)