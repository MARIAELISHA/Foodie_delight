from django.db import models
from django import forms
from django.contrib.auth.models import AbstractUser


# Create your models here.

class Food(models.Model):
    title = models.CharField(max_length=200)
    description=models.TextField()
    food_image=models.ImageField(upload_to='product')

    def __str__(self):
        return self.title
    
class LoginForm(forms.Form):
    username = forms.CharField()
    email=forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)  

class RecommendForm(forms.Form):
        new_food_item = forms.CharField(max_length=200)    


