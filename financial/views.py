from django.contrib import messages
from django.shortcuts import render

from financial.forms import ChargeWalletForm
from misc import views


def live_currency(request):
    return views.about_us(request)


def currency_converter(request):
    return views.about_us(request)


def online_wallet(request):
    charge_form = ChargeWalletForm(
        user=request.user,
        data=request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST':
        if charge_form.is_valid():
            charge_form.save()
            messages.add_message(request, messages.INFO, 'Account got charged successfully!')
    return views.render(request, 'financial/online_wallet.html', {'charge_wallet_form': charge_form})


def charged(request):
    return views.render(request, 'financial/charged.html')


def changed(request):
    return views.render(request, 'financial/changed.html')


def internal_payment(request):
    return views.render(request, 'financial/internal_payment.html')
