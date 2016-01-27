from django.contrib.auth.forms import  AuthenticationForm
from django.contrib.auth.models import User
from django import forms

class UserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="Nombre", required=False)
    last_name = forms.CharField(max_length=30, label="Apellido", required=False)
    username = forms.CharField(max_length=30, label="Usuario")
    password = forms.CharField(widget = forms.PasswordInput)
    email = forms.EmailField(label="Email", required=False)
    is_superuser = forms.BooleanField(label="Admin", required=False)

    class Meta():
        model = User
        fields = ['username', 'password', 'first_name', 'last_name', 'email', 'is_superuser'] 

class UpdateUserForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, label="Nombre", required=False)
    last_name = forms.CharField(max_length=30, label="Apellido", required=False)
    username = forms.CharField(max_length=30, label="Usuario")
    email = forms.EmailField(label="Email", required=False)
    is_superuser = forms.BooleanField(label="Admin", required=False)

    class Meta():
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'is_superuser'] 
