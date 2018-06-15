from django.shortcuts import render


def costumer_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


def employee_dashboard(request):
    return render(request, "workflow/employee_dashboard.html")
