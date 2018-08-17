from django.shortcuts import render


def costumer_dashboard(request):
    return render(request, "workflow/costumer_dashboard.html")


def employee_dashboard(request):
    return requests(request)


def requests(request):
    return render(request, 'workflow/requests_history.html')


def costumer_new_request(request):
    return render(request, "workflow/new_request.html")
