from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.db.models import Q
from django.contrib import messages

from financial.models import Transaction
from workflow.forms import UserNewRequestForm, UserNewRequestFromWithAmount, UserNewExchangeRequestFrom, \
    UserNewAnonymousRequestForm, CheckRequestForm
from workflow.models import RequestType, Request, ExchangeRequestType, ExchangeRequest, AnonymousRequest, ratio
from authorization.models import User


def costumer_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


@user_passes_test(lambda user: user.is_staff)
def employee_dashboard(request):
    return render(request, "workflow/employee_dashboard.html")


def user_requests_history(request, user_id=None):
    the_user = request.user
    if user_id is not None:
        the_user = User.objects.get(id=user_id)
    user_requests = Request.objects.filter(user=the_user)
    user_exchange_requests = ExchangeRequest.objects.filter(user=the_user)
    user_anonymous_requests = AnonymousRequest.objects.filter(src_user=the_user)
    return render(request, 'workflow/user_requests_history.html', {'user_requests': user_requests,
                                                                   'user_exchange_requests': user_exchange_requests,
                                                                   'user_anonymous_requests': user_anonymous_requests})


def user_request_history(request, num="1"):
    the_request = Request.objects.get(id=int(num))
    return render(request, 'workflow/user_request_history.html', {'request': the_request})


def user_exchange_request_history(request, num="1"):
    the_request = ExchangeRequest.objects.get(id=int(num))
    return render(request, 'workflow/user_exchange_request_history.html', {'request': the_request})


def user_anonymous_request_history(request, num="1"):
    the_request = AnonymousRequest.objects.get(id=int(num))
    return render(request, 'workflow/user_internal_payment_history.html', {'request': the_request})


def user_new_request(request, num="1"):
    request_type = RequestType.objects.get(id=int(num))
    if request_type.amount is not None:
        new_request_form = UserNewRequestForm(user=request.user, request_type=request_type,
                                              data=request.POST if request.method == 'POST' else None)
    else:
        new_request_form = UserNewRequestFromWithAmount(user=request.user, request_type=request_type,
                                                        data=request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if new_request_form.is_valid():
            new_request_form.save()
            if new_request_form.instance.transaction.status == Transaction.FAILED:
                messages.add_message(request, messages.INFO, 'Your Transaction Failed!')
            else:
                messages.add_message(request, messages.INFO, 'Your Request Submitted, Please Wait for the Employee!')
    return render(request, 'workflow/user_new_request.html', {'new_request_form': new_request_form,
                                                              'request_type': request_type})


def user_new_exchange_request(request, num="1"):
    exchange_request_type = ExchangeRequestType.objects.get(id=int(num))
    new_exchange_request_form = UserNewExchangeRequestFrom(user=request.user, request_type=exchange_request_type,
                                                           data=request.POST if request.method == 'POST' else None)
    if request.method == 'POST':
        if new_exchange_request_form.is_valid():
            # instance = new_exchange_request_form.instance
            # rate = ratio(instance.request_type.src_currency.name, instance.request_type.dst_currency.name)
            # amount = int(instance.amount) * rate
            new_exchange_request_form.save()
            if (new_exchange_request_form.instance.first_transaction.status == Transaction.SUCCEEDED) and (
                    new_exchange_request_form.instance.second_transaction.status == Transaction.SUCCEEDED):
                messages.add_message(request, messages.INFO, 'Your exchange request submitted successfully!')
            else:
                messages.add_message(request, messages.INFO, 'Your Transaction Failed!')
    return render(request, 'workflow/user_new_exchange_request.html',
                  {'new_exchange_request_form': new_exchange_request_form,
                   'exchange_request_type': exchange_request_type})


def user_request_types(request):
    request_types = RequestType.objects.all()
    return render(request, "workflow/user_request_types.html", context={'request_types': request_types})


def user_exchange_request_types(request):
    exchange_request_types = ExchangeRequestType.objects.all()
    return render(request, "workflow/user_exchange_request_types.html",
                  context={'exchange_request_types': exchange_request_types})


@user_passes_test(lambda user: user.is_staff)
def check_requests(request):
    user = request.user
    no_employee_requests = Request.objects.filter(employee=None).filter(status=Request.CREATED)
    his_requests = Request.objects.filter(employee=user)
    return render(request, "workflow/check_requests.html", {"no_employee_requests": no_employee_requests,
                                                            'his_requests': his_requests})


@user_passes_test(lambda user: user.is_staff)
def check_request(request, num="1"):
    the_request = Request.objects.get(id=int(num))
    the_request.employee = request.user
    the_request.save()
    if request.method == 'POST':
        check_request_form = CheckRequestForm(request.POST, instance=the_request)
        if check_request_form.is_valid():
            if check_request_form.cleaned_data['status'] == Request.SUCCEEDED:
                print('hi')
                the_request.transaction.status = Transaction.SUCCEEDED
            elif check_request_form.cleaned_data['status'] == Request.FAILED:
                the_request.transaction.status = Transaction.FAILED
            the_request.save()
            check_request_form.save()
            messages.add_message(request, messages.INFO, 'Request checked successfully!')
    else:
        check_request_form = CheckRequestForm(instance=the_request)
    return render(request, 'workflow/check_request.html', {'form': check_request_form,
                                                           'request': the_request})
