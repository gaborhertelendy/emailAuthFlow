# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class MyUserCreationForm(UserCreationForm):

    class Meta(UserCreationForm):
        model = User
        fields = ('email', 'password')


class MyUserChangeForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('email',)
