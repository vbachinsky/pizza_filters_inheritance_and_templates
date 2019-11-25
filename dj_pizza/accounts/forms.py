import re

from .models import User
from django import forms
from django.forms import ModelForm


class ChangePasswordForm(forms.Form):
    new_password = forms.CharField(required=True, max_length=50)
    password_repeat = forms.CharField(required=True, max_length=50)

    def clean(self):
        data = super(ChangePasswordForm, self).clean()
        if data.get('new_password') != data.get('password_repeat'):
            raise forms.ValidationError('Entered passwords must match!', None)
        return data


class RegistrationForm(forms.Form):
    email = forms.EmailField(required=True, max_length=50)
    password = forms.CharField(max_length=50)
    confirm_password = forms.CharField(max_length=50)
    terms = forms.BooleanField(required=False)

    def clean(self):
        data = super(RegistrationForm, self).clean()
        exist_user = User.exists(data.get('email'))
        if exist_user:
            self.add_error('email', 'User with this email already exist.')
        if data.get('password') != data.get('confirm_password'):
            self.add_error('confirm_password', 'Entered passwords must match!')
        return data



class UserForm(ModelForm):

    class Meta:
        model = User
        fields = ['first_name', 'last_name',]
