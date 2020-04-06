import json
import urllib

from database.models import *
from database.serializers import LABEL_TRANSLATIONS
from database.viewsets import object_map

from django.contrib.auth.decorators import login_required
from django.core.cache import cache
from django.http import Http404, HttpResponseRedirect, JsonResponse
from django.shortcuts import render

from mysite import configurations, extensions, graphics

NAVBAR_STRUCTURE = {
    "resources": [
        "product",
        "brand",
        "appliance",
        "organization",
        "organization_storage",
        "storage_product",
        "input",
        "output",
    ],
    "purchases": [
        "provider",
        "order",
        "invoice",
    ],
    "sales": [
        "customer",
        "pricelist",
        "percentage",
        "quotation",
        "sell",
    ],
    "hr": [
        "employee",
        "work",
    ],
    "reports": [],
}


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
        table_title = object_map[name]["name"]
        if not obj_id:
            scripts = []
            actions = [] if object_map[name].get('remove_reg_actions') else graphics.Action.edit_and_delete()
            buttons = [] if object_map[name].get('remove_table_actions') else graphics.Action.new_and_multidelete()
            actions.extend(object_map[name].get('custom_reg_actions', []))
            buttons.extend(object_map[name].get('custom_table_actions', []))
            filter_form = object_map[name].get('filter_form', None)
            if filter_form:
                if not request.GET:
                    filters = {x: y.initial for x, y in filter_form.fields.items()}
                    return HttpResponseRedirect(request.get_full_path()+"?"+urllib.parse.urlencode(filters))
                for key in request.GET.keys():
                    filter_form.fields[key].initial = request.GET[key]
            inline_script = "var prefetch = "+json.dumps(object_map[name].get('prefetch', []))+";\n"
            inline_script += "var actions = "+json.dumps([a.__dict__ for a in actions])+";\n"
            contents = []
            for action in actions+buttons:
                content = None
                if action.name in object_map[name]['action_forms'].keys():
                    content = object_map[name]['action_forms'][action.name]()
                if action.name in object_map[name].get('action_content', {}).keys():
                    content = object_map[name]['action_content'][action.name]
                if action.action == 'modal':
                    body = []
                    if content:
                        body.append(content)
                    modal = graphics.Modal.from_action(action, body, api_url=object_map[name]['api_path'])
                    contents.append(modal)
            scripts.extend(object_map[name].get('js', []))
        else:
            rendered = render_sheet(request, name, obj_id)
            return rendered
    else:
        raise Http404("Page does not exist")
    navbar_active = get_navbar_active(name)
    global_messages = get_cache_messages(name)
    return render(request, 'pages/dashboard.html', locals())


def get_cache_messages(name):
    messages = []
    for dep_obj in object_map[name].get('prefetch', []):
        obj_desc = object_map.get(dep_obj)
        if obj_desc:
            update_tsp = cache.get(obj_desc['model'].__name__)
            if update_tsp:
                messages.append(extensions.Message("update-{}".format(dep_obj), update_tsp))
    return messages


def get_navbar_active(name):
    active = {}
    active[name] = "active"
    for key, value in NAVBAR_STRUCTURE.items():
        if name in value:
            active[key] = "active"
            break
    return active


def render_sheet(request, name, obj_id):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    scripts = ["sheet_{}".format(name)]
    rest_url = object_map[name]['api_path']
    desc_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_desc', object_map[name].get('table_fields', []))])
    cont_fields = dict([(field, {"label": LABEL_TRANSLATIONS.get(field, field)}) for field in object_map[name].get('sheet_cont', [])])
    sheet = graphics.DescriptionSheet(
        name+"-sheet",
        object_map[name].get('sheet_name', object_map[name]['name']),
        obj_id,
        desc_fields=desc_fields,
        cont_fields=cont_fields,
        use_rest=rest_url,
    )
    contents = [sheet]
    return render(request, 'pages/dashboard.html', locals())

@login_required
def merge(request, name, obj_id):
    ids = json.loads(request.POST.get("ids"))
    if len(ids) > 1:
        real = object_map[name]['model'].objects.get(id=obj_id)
        ids.remove(int(obj_id))
        old = object_map[name]['model'].objects.filter(id__in=ids)
        for obj in old:
            if name == "customer":
                for sell in Sell.objects.filter(customer=obj):
                    sell.customer = real
                    sell.save()
                for pl in PriceList.objects.filter(customer=obj):
                    pl.customer = real
                    pl.save()
                for q in Quotation.objects.filter(customer=obj):
                    q.customer = real
                    q.save()
                for o in Output.objects.filter(destination=obj):
                    o.destination = real
                    o.save()
            obj.delete()
    return JsonResponse({"resp": request.POST})


@login_required
def reports(request, name):
    PAGE_TITLE = "Reportes"
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    navbar_active = {"reports": "active"}
    sidebar_active = {}
    if not name:
        scripts = ["reports", "reports_weekly"]
        global_messages = get_cache_messages("customer")
        sidebar_active["reports"] = 'active'
        return render(request, 'pages/reports.html', locals())
    else:
        scripts = ["reports", "reports_{}".format(name)]
        sidebar_active[name] = 'active'
        return render(request, 'pages/reports.html', locals())
    raise Http404("Page does not exist")


@login_required
def index(request):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    return render(request, 'pages/dashboard.html', locals())
