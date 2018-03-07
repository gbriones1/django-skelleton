from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect

from mysite.extensions import Notification, Message
from database.models import Configuration
from settings.forms import ConfigurationForm
from mysite.email_client import send_email

@login_required
def main(request):
    config = Configuration.objects.all()
    notifications = []
    if request.method == 'POST':
        form = ConfigurationForm(request.POST)
        if form.is_valid():
            if not config:
                Configuration.objects.get_or_create(**form.cleaned_data)
            else:
                new_pass = request.POST.get('password')
                if new_pass:
                    config[0].password = new_pass
                config[0].sender_email = request.POST.get('sender_email')
                new_quotation_pass = request.POST.get('quotations_password')
                if new_quotation_pass:
                    config[0].quotations_password = new_quotation_pass
                config[0].quotations_email = request.POST.get('quotations_email')
                config[0].receiver_email = request.POST.get('receiver_email')
                config[0].save()
            if config[0].sender_email and not send_email(config[0].sender_email, config[0].password, [request.POST.get('receiver_email')], 'Configuracion Actualizada', "El correo {} sera usado para enviar pedidos".format(config[0].sender_email)):
                notifications.append(Notification(message="Email para pedidos incorrecto. Use cuenta de gmail y password correctos", level="danger"))
            if config[0].quotations_email and not send_email(config[0].quotations_email, config[0].quotations_password, [request.POST.get('receiver_email')], 'Configuracion Actualizada', "El correo {} sera usado para enviar cotizaciones".format(config[0].sender_email)):
                notifications.append(Notification(message="Email para cotizaciones incorrecto. Use cuenta de gmail y password correctos", level="danger"))
        else:
            notifications.append(Notification(message=str(form.errors), level="danger"))
        if not notifications:
            return HttpResponseRedirect(request.get_full_path())
    form = ConfigurationForm()
    if config:
        form = ConfigurationForm(instance=config[0])
    return render(request, 'pages/settings.html', locals())
