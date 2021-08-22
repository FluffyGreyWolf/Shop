from django.contrib.auth import models
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from shop.models import userProfile

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

# Form for changing user profile picture
class changePictureForm(ModelForm):
    class Meta:
        model = userProfile
        fields = ['profile_picture']

class changeUsernameForm(ModelForm):
    username = forms.CharField(widget=forms.TextInput, label=False)
    class Meta:
        model = User
        fields = ['username']
        help_texts = {
            'username': None,
        }