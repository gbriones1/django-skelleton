from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

import time
import json

from warehouse.models import Provider, Brand, Appliance, Product, Percentage, Organization, Input, Output, Lending, Order
from warehouse.forms import (
    NewProductForm, EditProductForm, DeleteProductForm,
    NewProviderForm, EditProviderForm, DeleteProviderForm,
    NewBrandForm, EditBrandForm, DeleteBrandForm,
    NewApplianceForm, EditApplianceForm, DeleteApplianceForm,
    NewPercentageForm, EditPercentageForm, DeletePercentageForm,
    NewOrganizationForm, EditOrganizationForm, DeleteOrganizationForm,
    NewInputForm, EditInputForm, DeleteInputForm,
    NewOutputForm, EditOutputForm, DeleteOutputForm,
    NewLendingForm, EditLendingForm, DeleteLendingForm,
    NewOrderForm, EditOrderForm, DeleteOrderForm
)
from warehouse.serializers import ProviderSerializer, BrandSerializer, ApplianceSerializer, ProductSerializer, PercentageSerializer, OrganizationSerializer, InputSerializer, OutputSerializer, LendingSerializer, OrderSerializer
from mysite import configurations, graphics
from mysite.extensions import Notification, Message

@login_required
def main(request, name):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = []
    notifications = []
    global_messages = []
    scripts = ["tables"]
    if name == 'product':
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'new':
                vs = ProductViewSet.as_view({'post': 'create'})(request)
            elif action == 'edit':
                request.method = 'PUT'
                vs = ProductViewSet.as_view({'put': 'update'})(request, pk=request.POST.get('id'))
            elif action == 'delete':
                request.method = 'DELETE'
                vs = ProductViewSet.as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
            elif action == 'multi-delete':
                request.method = 'DELETE'
                ids = json.loads(request.POST.get('ids', '[]'))
                for pk in ids:
                    vs = ProductViewSet.as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
            if vs and vs.status_code/100 != 2:
                notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set('product-table-update', int(time.time()*1000))
                return HttpResponseRedirect(request.get_full_path())
        actions = graphics.Action.edit_and_delete()
        buttons = graphics.Action.new_and_multidelete()
        table = graphics.Table(
            "product-table",
            "Refacciones",
            Product.get_fields(),
            actions=actions,
            buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
            use_rest='/warehouse/api/product/'
        )
        contents = [table]
        for action in actions+buttons:
            body = []
            if action.name == "new":
                body = [NewProductForm()]
            elif action.name == "edit":
                body = [EditProductForm()]
            elif action.name == 'delete':
                body = [DeleteProductForm()]
            elif action.name == 'multi-delete':
                body = [graphics.MultiDeleteInput, graphics.MultiDeleteAction]
            modal = graphics.Modal.from_action(action, body)
            contents.append(modal)
        global_messages.append(Message(
            action='product-table-update',
            parameter=cache.get_or_set('product-table-update', int(time.time()*1000))
        ))
    # elif name == 'provider':
    #     providers = ProviderSerializer(Provider.objects.all(), many=True).data
    #     actions = graphics.Action.edit_and_delete()
    #     buttons = graphics.Action.new_and_multidelete()
    #     table = graphics.Table(
    #         "table-providers",
    #         "Provedores",
    #         Provider.get_fields(),
    #         actions=actions,
    #         buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
    #         rows=providers
    #     )
    #     contents = [table]
    #     for action in actions+buttons:
    #         contents.append(graphics.Modal.from_action(action))
    elif name in object_map.keys():
        if request.method == 'POST':
            action = request.POST.get('action')
            if action == 'new':
                vs = object_map[name]['viewset'].as_view({'post': 'create'})(request)
            elif action == 'edit':
                request.method = 'PUT'
                vs = object_map[name]['viewset'].as_view({'put': 'update'})(request, pk=request.POST.get('id'))
            elif action == 'delete':
                request.method = 'DELETE'
                vs = object_map[name]['viewset'].as_view({'delete': 'destroy'})(request, pk=request.POST.get('id'))
            if vs.status_code/100 != 2:
                notifications.append(Notification(message=str(vs.data), level="danger"))
            else:
                cache.set(name+'-table-update', int(time.time()*1000))
                return HttpResponseRedirect(request.get_full_path())
        actions = graphics.Action.edit_and_delete()
        buttons = graphics.Action.new_and_multidelete()
        table = graphics.Table(
            name+"-table",
            object_map[name]['name'],
            object_map[name]['model'].get_fields(),
            actions=actions,
            buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
            use_rest=object_map[name]['api_path']
        )
        contents = [table]
        for action in actions+buttons:
            content = None
            if action.name in object_map[name]['action_forms'].keys():
                content = object_map[name]['action_forms'][action.name]()
            modal = graphics.Modal.from_action(action, [content])
            contents.append(modal)
        global_messages.append(Message(
            action=name+'-table-update',
            parameter=cache.get_or_set(name+'-table-update', int(time.time()*1000))
        ))
    else:
        raise Http404("Page does not exist")
    return render(request, 'pages/warehouse.html', locals())

@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals())


class APIWrapper(viewsets.ModelViewSet):

    # def create(self, request, *args, **kwargs):
    #     serializer = self.get_serializer(data=request.data)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_create(serializer)
    #     headers = self.get_success_headers(serializer.data)
    #     return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def create(self, request, *args, **kwargs):
        # import pdb; pdb.set_trace()
        # obj = get_object_by('viewset', self.__class__)
        # resolve_foreign_fields(request.POST, obj['model'].get_fields())
        return super(APIWrapper, self).create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        return super(APIWrapper, self).update(request, *args, **kwargs)

    # def update(self, request, *args, **kwargs):
    #     return super(ProductViewSet, self).update(request, *args, **kwargs)
    #
    # def partial_update(self, request, *args, **kwargs):
    #     return super(ProductViewSet, self).partial_update(request, *args, **kwargs)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.order_by('name')
    serializer_class = ProviderSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.order_by('name')
    serializer_class = BrandSerializer

class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = Appliance.objects.order_by('name')
    serializer_class = ApplianceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.order_by('code')
    serializer_class = ProductSerializer

class PercentageViewSet(viewsets.ModelViewSet):
    queryset = Percentage.objects.order_by('max_price_limit')
    serializer_class = PercentageSerializer

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.order_by('name')
    serializer_class = OrganizationSerializer

class InputViewSet(viewsets.ModelViewSet):
    queryset = Input.objects.all()
    serializer_class = InputSerializer

class OutputViewSet(viewsets.ModelViewSet):
    queryset = Output.objects.all()
    serializer_class = OutputSerializer

class LendingViewSet(viewsets.ModelViewSet):
    queryset = Lending.objects.all()
    serializer_class = LendingSerializer

class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

# def get_object_by(attrib, match):
#     for name, value in object_map.items():
#         if object_map[name].get(attrib, None) == match:
#             return object_map[name]
#     return None
#
# def resolve_foreign_fields(data, fields):
#     data._mutable = True
#     for field in fields:
#         if field[2] == 'ForeignKey':
#             data[field[0]] = str(object_map[field[0]]['model'].objects.filter(name=data[field[0]])[0].pk)

object_map = {
    'product': {
        'name': 'Refacciones',
        'api_path': '/warehouse/api/product',
        'use_cache': True,
        'model': Product,
        'viewset': ProductViewSet,
        'action_forms': {
            'new': NewProductForm,
            'edit': EditProductForm,
            'delete': DeleteProductForm,
        }
    },
    'provider': {
        'name': 'Provedores',
        'api_path': '/warehouse/api/provider',
        'use_cache': True,
        'model': Provider,
        'viewset': ProviderViewSet,
        'action_forms': {
            'new': NewProviderForm,
            'edit': EditProviderForm,
            'delete': DeleteProviderForm,
        }
    },
    'brand': {
        'name': 'Marcas',
        'api_path': '/warehouse/api/brand',
        'use_cache': True,
        'model': Brand,
        'viewset': BrandViewSet,
        'action_forms': {
            'new': NewBrandForm,
            'edit': EditBrandForm,
            'delete': DeleteBrandForm,
        }
    },
    'appliance': {
        'name': 'Applicaciones',
        'api_path': '/warehouse/api/appliance',
        'use_cache': True,
        'model': Appliance,
        'viewset': ApplianceViewSet,
        'action_forms': {
            'new': NewApplianceForm,
            'edit': EditApplianceForm,
            'delete': DeleteApplianceForm,
        }
    },
    'percentage': {
        'name': 'Porcentajes',
        'api_path': '/warehouse/api/percentage',
        'use_cache': True,
        'model': Percentage,
        'viewset': PercentageViewSet,
        'action_forms': {
            'new': NewPercentageForm,
            'edit': EditPercentageForm,
            'delete': DeletePercentageForm,
        }
    },
    'organization': {
        'name': 'Organizaciones',
        'api_path': '/warehouse/api/organization',
        'use_cache': True,
        'model': Organization,
        'viewset': OrganizationViewSet,
        'action_forms': {
            'new': NewOrganizationForm,
            'edit': EditOrganizationForm,
            'delete': DeleteOrganizationForm,
        }
    },
    'input': {
        'name': 'Entradas',
        'api_path': '/warehouse/api/input',
        'use_cache': False,
        'model': Input,
        'viewset': InputViewSet,
        'action_forms': {
            'new': NewInputForm,
            'edit': EditInputForm,
            'delete': DeleteInputForm,
        }
    },
    'output': {
        'name': 'Salidas',
        'api_path': '/warehouse/api/output',
        'use_cache': False,
        'model': Output,
        'viewset': OutputViewSet,
        'action_forms': {
            'new': NewOutputForm,
            'edit': EditOutputForm,
            'delete': DeleteOutputForm,
        }
    },
    'lending': {
        'name': 'Prestamos',
        'api_path': '/warehouse/api/lending',
        'use_cache': False,
        'model': Lending,
        'viewset': LendingViewSet,
        'action_forms': {
            'new': NewLendingForm,
            'edit': EditLendingForm,
            'delete': DeleteLendingForm,
        }
    },
    'order': {
        'name': 'Pedidos',
        'api_path': '/warehouse/api/order',
        'use_cache': False,
        'model': Order,
        'viewset': OrderViewSet,
        'action_forms': {
            'new': NewOrderForm,
            'edit': EditOrderForm,
            'delete': DeleteOrderForm,
        }
    }
}
