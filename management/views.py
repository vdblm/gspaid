from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import messages
from authorization.models import User, SuperUser
from financial.models import Currency, Transaction
from management.models import Ticket
from management.forms import ContactAdminForm, ManageUserForm, NewRequestTypeForm, NewExchangeRequestTypeForm, \
    ManagementChargeWallet


@user_passes_test(lambda user: user.is_superuser)
def management_dashboard(request):
    return render(request, "management/management_dashboard.html")


@user_passes_test(lambda user: user.is_superuser)
def add_request_type(request):
    new_request_type_form = NewRequestTypeForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if new_request_type_form.is_valid():
            new_request_type_form.save()
            messages.add_message(request, messages.INFO, 'New Request Type Added')

    return render(request, 'management/new_request_type.html', {'new_request_type_from': new_request_type_form})


@user_passes_test(lambda user: user.is_superuser)
def add_exchange_request_type(request):
    new_exchange_request_type_form = NewExchangeRequestTypeForm(request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if new_exchange_request_type_form.is_valid():
            new_exchange_request_type_form.save()
            messages.add_message(request, messages.INFO, 'New Exchange Request Type Added')

    return render(request, 'management/new_exchange_request_type.html',
                  {'new_exchange_request_type': new_exchange_request_type_form})


@user_passes_test(lambda user: user.is_superuser)
def manage_profile(request, user_id):
    if request.method == 'POST':
        user_form = ManageUserForm(request.POST, instance=User.objects.get(id=user_id))
        if user_form.is_valid():
            user_form.save()
            messages.add_message(request, messages.INFO, 'Profile saved successfully!')
    else:
        user_form = ManageUserForm(instance=User.objects.get(id=user_id))
    return render(request, "management/manage_profile.html", {"user_form": user_form,
                                                              "user_id": user_id})


@user_passes_test(lambda user: user.is_superuser)
def comments(request):
    admin_comment = Ticket.objects.all()
    return render(request, "management/comments.html", {'comments': admin_comment})


@user_passes_test(lambda user: user.is_superuser)
def management_wallet(request):
    # Handle account balance
    currency_list = Currency.objects.all()
    user = SuperUser.get_solo()
    balance_list = [{'name': currency.name, 'value': float(calculate_balance(user, currency))} for currency in
                    currency_list]
    charge_form = ManagementChargeWallet(
        user=user,
        data=request.POST if request.method == 'POST' else None
    )
    if request.method == 'POST':
        if charge_form.is_valid():
            charge_form.save()
            messages.add_message(request, messages.INFO, 'Account got charged successfully!')
    return render(request, 'management/management_wallet.html', {'charge_wallet_form': charge_form,
                                                                 'balance_list': balance_list})


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


@user_passes_test(lambda user: user.is_superuser)
def management_users(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'management/users.html', {'users': users})


@user_passes_test(lambda user: user.is_superuser)
def management_employees(request):
    employees = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'management/employees.html', {'employees': employees})


@user_passes_test(lambda user: user.is_superuser)
def requests_history(request):
    users = User.objects.filter(is_staff=False, is_superuser=False)
    return render(request, 'management/requests.html', {'users': users})


def currency_transactions(request):
    transactions = Transaction.objects.all()
    return render(request, 'management/transactions.html', {'transactions': transactions})


def transaction(request, tr_id):
    transaction = Transaction.objects.get(id=tr_id)
    return render(request, 'management/transaction.html', {'transaction': transaction})