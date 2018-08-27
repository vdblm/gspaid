from django.apps import apps
from django.conf import settings
from django.forms import ModelForm
from django.forms.utils import ErrorList

from financial.models import Transaction, Currency
from management.models import Ticket
from workflow.models import RequestType, ExchangeRequestType


class ContactAdminForm(ModelForm):
    class Meta:
        model = Ticket
        exclude = []


class NewRequestTypeForm(ModelForm):
    class Meta:
        model = RequestType
        fields = ['name', 'description', 'wage_rule', 'currency', 'amount', 'information', 'is_withdraw']


class NewExchangeRequestTypeForm(ModelForm):
    class Meta:
        model = ExchangeRequestType
        fields = ['name', 'description', 'wage_rule', 'src_currency', 'dst_currency']


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


class ManagementChargeWallet(ModelForm):
    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user

    class Meta:
        model = Transaction
        fields = ['to_amount', 'to_currency']

    def is_valid(self):
        self.instance.from_amount = 0
        self.instance.from_user = None
        self.instance.status = Transaction.SUCCEEDED
        self.instance.from_currency = Currency.objects.first()
        self.instance.to_user = self.user
        return super().is_valid()
