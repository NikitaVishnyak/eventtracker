from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django import forms

from users.models import CustomUsers


class RegisterUserForm(UserCreationForm):
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'first name'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'last name'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-input'}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'password'}))
    password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'confirm password'}))

    class Meta:
        model = CustomUsers
        fields = ('first_name', 'last_name', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.EmailField(widget=forms.EmailInput(attrs={'placeholder': 'email', 'class': 'form-input'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-input', 'placeholder': 'password'}))

    class Meta:
        model = CustomUsers
        fields = ('email', 'password')
