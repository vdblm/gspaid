from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django import forms
from django.forms.utils import ErrorList
from workflow.models import Request, ExchangeRequest, AnonymousRequest


class UserNewRequestForm(ModelForm):
    def __init__(self, user, request_type, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        if request_type is None:
            raise Exception('RequestType should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user
        self.request_type = request_type

    class Meta:
        model = Request
        fields = ['attachment', 'user_description']

    def is_valid(self):
        self.instance.request_type = self.request_type
        self.instance.user = self.user
        return super().is_valid()


class UserNewRequestFromWithAmount(ModelForm):
    def __init__(self, user, request_type, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        if request_type is None:
            raise Exception('RequestType should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user
        self.request_type = request_type

    class Meta:
        model = Request
        fields = ['attachment', 'user_description', 'amount']

    def is_valid(self):
        self.instance.request_type = self.request_type
        self.instance.user = self.user
        return super().is_valid()


class CheckRequestForm(ModelForm):
    class Meta:
        model = Request
        fields = ['status', 'employee_description']


class UserNewExchangeRequestFrom(ModelForm):
    def __init__(self, user, request_type, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        if request_type is None:
            raise Exception('RequestType should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user
        self.request_type = request_type

    class Meta:
        model = ExchangeRequest
        fields = ['amount']

    def is_valid(self):
        self.instance.request_type = self.request_type
        self.instance.user = self.user
        return super().is_valid()


class UserNewAnonymousRequestForm(ModelForm, forms.Form):
    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None,
                 error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user
        self.dst_user = None

    def set_dst_user(self, dst_user):
        self.dst_user = dst_user

    class Meta:
        model = AnonymousRequest
        fields = ['currency', 'amount']

    email = forms.EmailField()

    def is_valid(self):
        return super().is_valid()
