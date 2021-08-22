from django.contrib.auth import models
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from shop.models import userProfile

# Form for creating user
class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for changing user profile picture
class changePictureForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ['profile_picture']

# Form for changing user name
class changeUsernameForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput, label=False)
    class Meta:
        model = User
        fields = ['username']
        help_texts = {
            'username': None,
        }

# Form for changing user email
class changeEmailForm(ModelForm):
    email = forms.EmailField(widget=forms.EmailInput, label=False)
    class Meta:
        model = User
        fields = ['email']
        help_texts = {
            'email': None,
        }

# Form for changing user password
class changePasswordForm(ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, label='Enter password')
    password_conf = forms.CharField(widget=forms.PasswordInput, label='Confirm password')
    class Meta:
        model = User
        fields = ['password']
        help_texts = {
            'password': None,
        }