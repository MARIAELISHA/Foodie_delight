from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User
from django import forms
from .forms import RecommendForm




# Create your models here.

class Food(models.Model):
    title = models.CharField(max_length=200)
    description=models.TextField()
    food_image=models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  

class RecommendForm(forms.Form):
        new_food_item = forms.CharField(max_length=200)


