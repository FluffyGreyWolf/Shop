from django.contrib.auth import models
from django.forms import ModelForm, fields, widgets
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from shop.models import Review

class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(max_value=5, min_value=1, widget=forms.NumberInput(attrs={"placeholder": "Input rating from 1 to 5"}))
    content = forms.CharField(widget=forms.Textarea(attrs={"rows": 10, "cols": 60}), label=False)
    class Meta:
        model = Review
        fields = ["content", "rating"]
        help_texts = {
            'content': None,
            'rating': None,
        }