from django.apps import apps
from django.conf import settings
from django.forms.models import ModelForm


class UserForm(ModelForm):
    class Meta:
        model = apps.get_model(settings.AUTH_USER_MODEL)
        fields = [
            'first_name',
            'last_name',
            'phone_number',
            'email',
            'notification_is_enabled'
        ]
