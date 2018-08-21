from django.apps import apps
from django.conf import settings
from django.forms.models import ModelForm
from registration.forms import RegistrationForm


class UserForm(ModelForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'notification_type'
        ]


class GSPaidRegistrationForm(RegistrationForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = ['first_name', 'last_name', 'username', 'phone_number']