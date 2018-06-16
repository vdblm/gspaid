from django.shortcuts import render
from misc import views


def live_currency(request):
    return views.about_us(request)


def currency_converter(request):
    return views.about_us(request)

