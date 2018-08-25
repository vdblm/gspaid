from django.apps import apps
from django.conf import settings
from django.forms import ModelForm

from management.models import Ticket


class ContactAdminForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = []


class ManageUserForm(ModelForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'notification_type',
            'is_staff',
            'is_superuser',
            'salary',
        ]