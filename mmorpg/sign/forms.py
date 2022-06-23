from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()

    # class Meta allows us to connect to an existing model and adjust its fields
    class Meta:
        # here we specify a model this form is going to interact with
        # because since this form passes validation, it creates a new user model instance
        # form.save() from views creates this model instance
        model = User
        # and adds these fields to the model instance
        fields = ['username', 'email', 'password1', 'password2']


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ["username", "email"]


class ProfileUpdateForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ["image"]