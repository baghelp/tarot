from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class DeleteAccountForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username',)

    def __init__(self, *args, **kwargs):
        self.expected_username = kwargs.pop('username', None)
        super(DeleteAccountForm, self).__init__(*args, **kwargs)
        self.fields['username'].help_text = 'type your username to confirm account deletion'

    def clean(self, *args, **kwargs):
        if self.cleaned_data.get('username') != self.expected_username:
            raise ValidationError('username does not match')


