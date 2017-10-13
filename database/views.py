from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect, HttpResponse
from django.template import RequestContext
from django.core.cache import cache

import time
import json
import urllib
import os
from datetime import datetime

from database.models import *
from database.serializers import *
from database.viewsets import *
from database.forms import *

from mysite import configurations, graphics
from mysite.extensions import Notification, Message
from mysite.email_client import send_email

@login_required
def main(request, name, obj_id):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = []
    notifications = []
    global_messages = []
    if name in object_map.keys():
        cache_name = name+"-"+urllib.urlencode(request.GET)
        if request.method == 'POST':
            action = request.POST.get('action')
            vs = None
            if action == 'new':
                vs = object_map[name]['viewset'].as_view({'post': 'create'})(request)
            elif action == 'edit':
                request.method = 'PUT'
                vs = object_map[name]['viewset'].as_view({'put': 'update'})(request, pk=request.POST.get('id'))
            elif action == 'delete':
                request.method = 'DELETE'
                vs = object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
            elif action == 'multi-delete':
                request.method = 'DELETE'
                request.POST._mutable = True
                ids = json.loads(request.POST.get('ids', '[]'))
                for pk in ids:
                    request.POST['id'] = pk
                    vs = object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
                if not ids:
                    notifications.append(Notification(message="No elements selected", level="danger"))
            elif action:
                vs = object_map[name]['viewset'].as_view({'post': action})(request)
            if vs and vs.status_code/100 != 2:
                if hasattr(vs.data, 'iterkeys'):
                    for key in vs.data.keys():
                        notifications.append(Notification(message=str(key)+": "+str(vs.data[key]), level="danger"))
                elif type(vs.data) == type([]):
                    for error in vs.data:
                        notifications.append(Notification(message=str(error), level="danger"))
                else:
                    notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set(cache_name+'-table-update', int(time.time()*1000))
                redirect = request.get_full_path()
                if hasattr(vs, "redirect_to"):
                    redirect = vs.redirect_to
                return HttpResponseRedirect(redirect)
        rest_url = object_map[name]['api_path']
        if request.GET:
            rest_url += "?"+urllib.urlencode(request.GET)
        add_fields = object_map[name].get('add_fields', [])
        remove_fields = object_map[name].get('remove_fields', [])
        if not obj_id:
            scripts = ["tables"]
            actions = [] if object_map[name].get('remove_reg_actions') else graphics.Action.edit_and_delete()
            buttons = [] if object_map[name].get('remove_table_actions') else graphics.Action.new_and_multidelete()
            actions.extend(object_map[name].get('custom_reg_actions', []))
            buttons.extend(object_map[name].get('custom_table_actions', []))
            filter_form = object_map[name].get('filter_form', None)
            use_cache = object_map[name].get('use_cache', True)
            if filter_form:
                if not request.GET:
                    filters = {x:y.initial for x,y in filter_form.fields.items()}
                    return HttpResponseRedirect(request.get_full_path()+"?"+urllib.urlencode(filters))
                for key in request.GET.keys():
                    filter_form.fields[key].initial = request.GET[key]
            checkbox = False if object_map[name].get('remove_checkbox') else True
            table = graphics.Table(
                cache_name+"-table",
                object_map[name]['name'],
                object_map[name]['model'].get_fields(remove_fields=remove_fields, add_fields=add_fields),
                actions=actions,
                buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
                use_rest=rest_url,
                use_cache=use_cache,
                checkbox=checkbox,
            )
            contents = [table]
            for action in actions+buttons:
                content = None
                if action.name in object_map[name]['action_forms'].keys():
                    content = object_map[name]['action_forms'][action.name]()
                modal = graphics.Modal.from_action(action, [content])
                contents.append(modal)
            global_messages.append(Message(
                action=cache_name+'-table-update',
                parameter=cache.get_or_set(cache_name+'-table-update', int(time.time()*1000))
            ))
            scripts.extend(object_map[name].get('js', []))
        else:
            scripts = ["sheets"]
            sheet = graphics.DescriptionSheet(
                cache_name+"-sheet",
                object_map[name]['name'],
                obj_id,
                object_map[name]['model'].get_fields(remove_fields=remove_fields, add_fields=add_fields),
                use_rest=rest_url,
            )
            contents = [sheet]
    else:
        raise Http404("Page does not exist")
    # start_time = time.time()
    # response = render(request, 'pages/database.html', locals())
    # elapsed_time = time.time() - start_time
    # print(elapsed_time)
    return render(request, 'pages/database.html', locals())


@login_required
def reports(request, name):
    PAGE_TITLE = "Reportes"
    if not name:
        APPNAME = configurations.APPNAME
        YEAR = configurations.YEAR
        VERSION = configurations.VERSION
        contents = [
            graphics.Table("reports-table", "Reportes", [("name", "Nombre")], rows=[
                {"name":"Finanzas de almacen", "report":"storage_finance"},
                {"name":"Deudas de facturas", "report":"invoice_debts"},
                {"name":"Unidades mas conflictivas"},
                {"name":"Clientes mas rentables"}
            ],
            actions=[graphics.Action("view", 'script', icon='eye', style='info')],
            checkbox=False, use_cache=False)
        ]
        scripts = ["reports_index"]
        return render(request, 'pages/database.html', locals())
    else:
        if name == "invoice_debts":
            today = datetime.now()
            unpaid = Invoice.objects.filter(paid=False)
            filter_form = InvoiceProviderFilterForm()
            provider_id = request.GET.get('provider')
            if provider_id:
                unpaid = unpaid.filter(provider=provider_id)
                filter_form.fields['provider'].initial = provider_id
            unpaid_rows = [InvoiceSerializer(x).data for x in unpaid]
            expired = unpaid.filter(due__lte=today)
            expired_rows = [InvoiceSerializer(x).data for x in expired]
            soon = unpaid.filter(due__gt=today)
            contents = [
                graphics.Table(name, "Facturas vencidas", Invoice.get_fields(remove_fields=['provider'], add_fields=[('provider_name', 'Provider', 'CharField')]), rows=expired_rows, checkbox=False, use_cache=False),
                graphics.Table(name, "Facturas sin pagar", Invoice.get_fields(remove_fields=['provider'], add_fields=[('provider_name', 'Provider', 'CharField')]), rows=unpaid_rows, checkbox=False, use_cache=False),
            ]
        return render(request, 'pages/database.html', locals())
    raise Http404("Page does not exist")

@login_required
def special_api(request, name):
    print(name)
    if name == 'instorage':
        storage_product = {}
        for sp in Storage_Product.objects.filter(amount__gt=0):
            storage_product.setdefault(sp.organization_storage.id, {}).setdefault(sp.product.id, sp.amount)
        return HttpResponse(json.dumps(storage_product), content_type="application/json")
    elif name == 'pricelistrelated':
        related = {}
        for pp in PriceList_Product.objects.all():
            related.setdefault(pp.pricelist.id, {}).setdefault(pp.product.id, float(pp.price))
        return HttpResponse(json.dumps(related), content_type="application/json")
    raise Http404("Page does not exist")


@login_required
def index(request):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    return render(request, 'pages/database.html', locals())


@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals())
