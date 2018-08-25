from django.shortcuts import render
from django.contrib import messages
from workflow.forms import UserNewRequestForm, UserNewRequestFromWithAmount
from workflow.models import RequestType, Request


def costumer_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


# Temporary
def employee_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


def user_requests_history(request):
    user_requests = Request.objects.filter(user=request.user)
    return render(request, 'workflow/user_requests_history.html', {'user_requests': user_requests})


def user_request_history(request, num="1"):
    the_request = Request.objects.get(id=int(num))
    return render(request, 'workflow/user_request_history.html', {'request': the_request})


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
            messages.add_message(request, messages.INFO, 'Your request submitted successfully!')
    return render(request, 'workflow/user_new_request.html', {'new_request_form': new_request_form,
                                                              'request_type': request_type})


def user_request_types(request):
    request_types = RequestType.objects.all()
    return render(request, "workflow/user_request_types.html", context={'request_types': request_types})
