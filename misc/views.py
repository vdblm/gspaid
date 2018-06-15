from django.shortcuts import render
from management import views as management_views
from workflow import views as workflow_views


def about_us(request):
    return render(request, "misc/home.html")


def rules(request):
    return render(request, "misc/rules.html")


def dashboard(request):
    if request.user.is_superuser:
        return management_views.dashboard(request)

    if request.user.is_staff:
        return workflow_views.employee_dashboard(request)

    return workflow_views.costumer_dashboard(request)