from dataclasses import fields

from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Profile
# from crispy_forms.helper import FormHelper


class CreateUserForm(UserCreationForm):
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.helper = FormHelper(self)

    class Meta :
        model = User
        fields = ['username' , 'email' , 'password1' , 'password2']

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image', 'biography', 'preferences']


# as far as I can tell this might be where I should start for dynamic email
