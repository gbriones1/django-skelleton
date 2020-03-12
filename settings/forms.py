from django import forms

from database.models import Configuration
from mysite.forms import *

class EmailsForm(forms.ModelForm):
    sender_email = forms.CharField(required=False, label="Email para pedidos")
    password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password del email para pedidos")
    quotations_email = forms.CharField(required=False, label="Email para cotizaciones")
    quotations_password = forms.CharField(widget=forms.PasswordInput(), required=False, label="Password del email para cotizaciones")
    receiver_email = forms.CharField(required=False, label="Email para notificaciones")
    action = HiddenField(initial="emails")

    class Meta:
        model = Configuration
        fields = (
            'sender_email',
            'password',
            'quotations_email',
            'quotations_password',
            'receiver_email'
        )

class ReportsForm(forms.ModelForm):
    week_cut = forms.ChoiceField(label="Corte Semanal", choices=Configuration.WEEK_DAYS)
    action = HiddenField(initial="reports")
    class Meta:
        model = Configuration
        fields = (
            'week_cut',
        )