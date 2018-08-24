from django.shortcuts import render
from workflow.forms import UserRequestForm


def costumer_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


# Temporary
def employee_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


def user_requests(request):
    request_form = UserRequestForm(
            user=request.user,
            data=request.POST if request.method == "POST" else None
        )
    if request.method == "POST":
        if request_form.is_valid():
            request_form.save()
    return render(request, 'workflow/requests_history.html')


def costumer_new_request(request):
    return render(request, "workflow/new_request.html")
