from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)
    email = forms.EmailField(max_length=200, required=True)
    password = forms.CharField( max_length=40, required=True)

class SignInForm(forms.Form):
    username = forms.CharField(max_length=150, required=True)

    # email = forms.EmailField(max_length=200)
    password = forms.CharField(widget=forms.PasswordInput)

