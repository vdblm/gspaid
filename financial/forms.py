from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.utils import ErrorList

from financial.models import Transaction, Currency


class ChargeWalletForm(ModelForm):
    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user

    class Meta:
        model = Transaction
        fields = ['to_amount']

    def is_valid(self):
        self.instance.from_amount = 0
        self.instance.from_user = None
        self.instance.status = Transaction.SUCCEEDED
        self.instance.from_currency = Currency.objects.get(name='IRR')
        self.instance.to_currency = Currency.objects.get(name='IRR')
        self.instance.to_user = self.user
        if int(self.data['to_amount']) < 1000:
            raise ValidationError('Amount should be more that or equal to 1000.')
        return super().is_valid()
