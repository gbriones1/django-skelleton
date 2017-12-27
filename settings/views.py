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
                config[0].receiver_email = request.POST.get('receiver_email')
                config[0].save()
            if send_email(request.POST.get('receiver_email'), 'Bienvenido', "Esta direccion de correo es la que se va a usar para recibir notificaciones de la base de datos de Muelles Obrero"):
                return HttpResponseRedirect(request.get_full_path())
            else:
                notifications.append(Notification(message="Configuracion de email incorrecta. Use cuenta de gmail y password correctos", level="danger"))
        else:
            notifications.append(Notification(message=str(form.errors), level="danger"))
    form = ConfigurationForm()
    if config:
        form = ConfigurationForm(instance=config[0])
    return render(request, 'pages/settings.html', locals())
