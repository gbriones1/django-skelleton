from django import forms

from database.models import Configuration

class ConfigurationForm(forms.ModelForm):
    sender_email = forms.CharField(required=False, label="Email para pedidos")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password del email para pedidos")
    quotations_email = forms.CharField(required=False, label="Email para cotizaciones")
    quotations_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password del email para cotizaciones")
    receiver_email = forms.CharField(required=False, label="Email para notificaciones")

    class Meta:
        model = Configuration
        fields = (
            'sender_email',
            'password',
            'quotations_email',
            'quotations_password',
            'receiver_email'
        )
