from django.contrib import admin

# Register your models here.
from solo.admin import SingletonModelAdmin
from .models import ExchangeRequest

admin.site.register(ExchangeRequest, SingletonModelAdmin)
