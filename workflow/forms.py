from django.core.exceptions import ValidationError
from django.forms import ModelForm
from django.forms.utils import ErrorList
from workflow.models import Request


class UserRequestForm(ModelForm):
    def __init__(self, user, data=None, files=None, auto_id='id_%s', prefix=None, initial=None, error_class=ErrorList,
                 label_suffix=None, empty_permitted=False, instance=None, use_required_attribute=None):
        if user is None:
            raise Exception('User should be defined.')
        super().__init__(data, files, auto_id, prefix, initial, error_class, label_suffix, empty_permitted, instance,
                         use_required_attribute)
        self.user = user

    class Meta:
        model = Request
        fields = ['attachment', 'user_description']

    def is_valid(self):
        self.instance.user = self.user
        return super().is_valid()
