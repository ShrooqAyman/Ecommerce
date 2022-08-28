from dataclasses import fields
import email
from re import U
from django import forms
from .models import UserBase
from django.contrib.auth.forms import AuthenticationForm,PasswordResetForm,SetPasswordForm

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


class UserEditForm(forms.ModelForm):
    email = forms.EmailField(label='Account Email(can not be changed )', widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'email', 'id':'email' ,'readonly':'readonly'}))
    user_name = forms.CharField(label='username',widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'Username', 'id':'user_name'}))
    first_name = forms.CharField(label='first name',widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'First Name', 'id':'first_name'}))

    class Meta:
        model = UserBase
        fields = ('user_name', 'email', 'first_name')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(label=' Email', widget=forms.TextInput(attrs={'class':'form-control mb-3', 'placeholder':'email', 'id':'email'}))
    def clean_email(self):
        email = self.cleaned_data['email']
        if not (UserBase.objects.filter(email=email)):
            raise forms.ValidationError('unfortunately we can not find that email address')
        return email
    
class PwdResetConfirmForm(SetPasswordForm):
    new_password = forms.CharField(label=' Password',widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Password', 'id':'pwd1'}))
    new_password2 = forms.CharField(label='Repeat Password',widget=forms.PasswordInput(attrs={'class':'form-control mb-3', 'placeholder':'Repeat Password', 'id':'pwd2'}))
