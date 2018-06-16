from django.shortcuts import render
from django.contrib import messages

from management.forms import ContactAdminForm


def contact_admin(request):
    if request.method == 'POST':
        form = ContactAdminForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Sent message to admin.")
    else:
        form = ContactAdminForm()

    return render(
        request,
        template_name='management/contact_admin.html',
        context={
            'form': form
        }
    )


def dashboard(request):
    return render(request, "management/management_dashboard.html")


def add_request_type(request):
    return render(request, 'management/new_request_type.html')
