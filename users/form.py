from django import forms
from .models import User

class UserForm(forms.ModelForm):
    email =  forms.CharField(min_length=10, max_length=10)