from django.contrib.auth.models import User
from django import forms
from .models import *


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=100)
    password = forms.CharField(label="Password", widget=forms.PasswordInput())        

class RecommendForm(forms.Form):
    new_food_item = forms.CharField(max_length=100, label='new_food_item')