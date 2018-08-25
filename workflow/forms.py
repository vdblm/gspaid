from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.utils import ErrorList
from workflow.models import Request


class UserNewRequestForm(ModelForm):
    def __init__(self, user, request_type, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
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
    def __init__(self, user, request_type, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
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

