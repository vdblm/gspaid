from _random import Random

from django.contrib import messages
from django.core.mail import send_mail
from django.db.models import QuerySet
from django.shortcuts import render

from authorization.models import User
from financial.forms import ChargeWalletForm
from financial.models import Transaction, Currency
from misc import views
from workflow.forms import UserNewAnonymousRequestForm


def live_currency(request):
    return views.about_us(request)


def currency_converter(request):
    return views.about_us(request)


def calculate_balance(user, currency):
    input_transactions = Transaction.objects.filter(to_user=user).filter(to_currency=currency).filter(
        status=Transaction.SUCCEEDED)
    output_transactions = Transaction.objects.filter(from_user=user).filter(from_currency=currency).filter(
        status=Transaction.SUCCEEDED)

    input_amount = 0
    output_amount = 0
    for transaction in input_transactions:
        input_amount = input_amount + transaction.to_amount
    for transaction in output_transactions:
        output_amount = output_amount + transaction.from_amount

    return input_amount - output_amount


def online_wallet(request):
    # Handle account balance
    currency_list = Currency.objects.all()
    balance_list = [{'name': currency.name, 'value': float(calculate_balance(request.user, currency))} for currency in
                    currency_list]
    charge_form = ChargeWalletForm(
        user=request.user,
        data=request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST':
        if charge_form.is_valid():
            charge_form.save()
            messages.add_message(request, messages.INFO, 'Account got charged successfully!')
    return views.render(request, 'financial/online_wallet.html', {'charge_wallet_form': charge_form,
                                                                  'balance_list': balance_list})


def charged(request):
    return views.render(request, 'financial/charged.html')


def internal_payment(request):
    new_anonymous_request_form = UserNewAnonymousRequestForm(user=request.user,
                                                             data=request.POST if request.method == 'POST' else None)
    if request.method == 'POST' and new_anonymous_request_form.is_valid():
        # Logic for finding dst user and set form's.
        dst_user_email = new_anonymous_request_form.cleaned_data['email']
        dst_user = User.objects.filter(email=dst_user_email)
        if dst_user.exists():
            dst_user = dst_user[0]
        else:
            random = Random()
            password = str(int(random.random() * 100000)) + 'pass'
            send_mail('You have received money',
                      'Please go to website ... and complete your profile. Your user name is your email. Your '
                      'pass: ' + password, 'gspaid.company@gmail.com', [dst_user_email], fail_silently=False)
            dst_user = User.objects.create_user(email=dst_user_email, username=dst_user_email, password=password)
        new_anonymous_request_form.set_dst_user(dst_user)
        new_anonymous_request_form.instance.src_user = new_anonymous_request_form.user
        new_anonymous_request_form.instance.dst_user = new_anonymous_request_form.dst_user
        new_anonymous_request_form.save()
        if new_anonymous_request_form.instance.transaction.status == Transaction.SUCCEEDED:
            messages.add_message(request, messages.INFO, 'Your anonymous request submitted successfully!')
        else:
            messages.add_message(request, messages.INFO, 'Your Transaction Failed!')
    return render(request, 'financial/internal_payment.html',
                  {'new_anonymous_request_form': new_anonymous_request_form})
