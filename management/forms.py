from django.forms import ModelForm
from management.models import Ticket
from workflow.models import RequestType


class ContactAdminForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = []


class NewRequestTypeForm(ModelForm):
    class Meta:
        model = RequestType
        fields = ['name', 'description', 'wage_rule', 'currency', 'amount', 'information']

    def is_valid(self):
        self.instance.user = self.user
        return super().is_valid()
