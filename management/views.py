from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render
from django.contrib import messages
from authorization.models import User
from management.forms import ContactAdminForm, ManageUserForm, NewRequestTypeForm


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


def settings(request):
    return render(request, 'management/settings.html')


def settings_changed(request):
    return render(request, 'management/settings_changed.html')


@user_passes_test(lambda user: user.is_superuser)
def manage_profile(request, user_id):
    if request.method == 'POST':
        user_form = ManageUserForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            messages.add_message(request, messages.INFO, 'Profile saved successfully!')
    else:
        user_form = ManageUserForm(instance=User.objects.get(id=user_id))
    return render(request, "edit_user_info/profile.html", {"user_form": user_form})
