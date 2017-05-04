from django import forms

from database.models import Configuration

class ConfigurationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(), required=False)

    class Meta:
        model = Configuration
        fields = '__all__'
