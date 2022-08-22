from dataclasses import fields
import email
from re import U
from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Username', 'id':'login-username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Password', 'id':'login-pwd'}))

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(label="Enter username", min_length=4, max_length=50, help_text="Required")
    email = forms.EmailField(max_length=100, help_text="required", error_messages={'required':'sorry, you will need an email'} )
    password = forms.CharField(label="password", widget=forms.PasswordInput)
    password2 = forms.CharField(label="Repeat Password", widget=forms.PasswordInput)

    class Meta:
        model = UserBase
        fields = ('user_name', 'email')

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = UserBase.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError('username is already exists')
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('passwords do not matche')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if UserBase.objects.filter(email=email).exists():
            raise forms.ValidationError('please use another email, that is already taken')
        return email
