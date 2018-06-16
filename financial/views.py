from django.shortcuts import render
from misc import views


def live_currency(request):
    return views.about_us(request)


def currency_converter(request):
    return views.about_us(request)


def online_wallet(request):
    return views.render(request, 'financial/online_wallet.html')


def charged(request):
    return views.render(request, 'financial/charged.html')


def changed(request):
    return views.render(request, 'financial/changed.html')
