from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from app.models import Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput) 


class RegistrationForm(UserCreationForm):
    profile_picture = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'profile_picture')