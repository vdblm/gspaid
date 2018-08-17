from django.forms import ModelForm

from management.models import Ticket


class ContactAdminForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = []
