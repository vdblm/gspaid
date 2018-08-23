from __future__ import unicode_literals

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from solo.models import SingletonModel


class User(AbstractUser):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in the format: "
                                                                   "'+999999999'. Up to 15 digits allowed.")
    phone_number = models.CharField(validators=[phone_regex], max_length=17, blank=False, null=False)

    EMAIL = 'email'
    SMS = 'sms'

    NOTIFICATION_CHOICES = (
        (EMAIL, 'Email'),
        (SMS, 'SMS'),
    )

    notification_type = models.CharField(max_length=8, choices=NOTIFICATION_CHOICES, default=EMAIL)


class SuperUser(User, SingletonModel):
    phone_number = "+989381137897"

