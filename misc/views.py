from django.contrib import messages
from django.shortcuts import render
from management import views as management_views
from workflow import views as workflow_views
from management.forms import ContactAdminForm


def about_us(request):
    user = request.user
    contact_admin_form = ContactAdminForm(request.POST)
    if request.method == 'POST':
        if contact_admin_form.is_valid():
            contact_admin_form.save()
            messages.success(request, "Sent message to admin.")
    return render(request, "misc/home.html", {'user': user,
                                              'contact_admin_form': contact_admin_form})


def rules(request):
    return render(request, "misc/rules.html")


def dashboard(request):
    if request.user.is_superuser:
        return management_views.management_dashboard(request)

    if request.user.is_staff:
        return workflow_views.employee_dashboard(request)

    return workflow_views.costumer_dashboard(request)
