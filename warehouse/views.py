from django.shortcuts import render, render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404, HttpResponseRedirect
from django.template import RequestContext
from django.core.cache import cache
from rest_framework import viewsets
from rest_framework.response import Response

import time

from warehouse.models import Provider, Brand, Appliance, Product, Organization
from warehouse.forms import NewProductForm, EditProductForm
from warehouse.serializers import ProviderSerializer, BrandSerializer, ApplianceSerializer, ProductSerializer, OrganizationSerializer
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
            pvs = ProductViewSet.as_view({'post': 'create'})(request)
            if pvs.status_code/100 != 2:
                notifications.append(Notification(message=str(pvs.data), level="danger"))
            else:
                cache.set('product-table-update', int(time.time()*1000))
                return HttpResponseRedirect(request.get_full_path())
        if request.method == 'PUT':
            pvs = ProductViewSet.as_view({'put': 'update'})(request)
            cache.get_or_set('product-table-update', int(time.time()*1000))
            return HttpResponseRedirect(request.get_full_path())
        if request.method == 'DELETE':
            pvs = ProductViewSet.as_view({'delete': 'destroy'})(request)
            cache.get_or_set('product-table-update', int(time.time()*1000))
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
            content = None
            if action.name == "new":
                content = NewProductForm()
            elif action.name == "edit":
                content = EditProductForm()
            modal = graphics.Modal.from_action(action, [content])
            import pdb; pdb.set_trace()
            contents.append(modal)
        global_messages.append(Message(
            action='product-table-update',
            parameter=cache.get_or_set('product-table-update', int(time.time()*1000))
        ))
    elif name == 'provider':
        providers = ProviderSerializer(Provider.objects.all(), many=True).data
        actions = graphics.Action.edit_and_delete()
        buttons = graphics.Action.new_and_multidelete()
        table = graphics.Table(
            "table-providers",
            "Provedores",
            Provider.get_fields(),
            actions=actions,
            buttons=[graphics.HTMLButton.from_action(action) for action in buttons],
            rows=providers
        )
        contents = [table]
        for action in actions+buttons:
            contents.append(graphics.Modal.from_action(action))
    else:
        raise Http404("Page does not exist")
    return render(request, 'pages/warehouse.html', locals())

@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals())


class APIWrapper(viewsets.ModelViewSet):

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        return super(ProductViewSet, self).update(request, *args, **kwargs)


class ProviderViewSet(viewsets.ModelViewSet):
    queryset = Provider.objects.all()
    serializer_class = ProviderSerializer

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer

class ApplianceViewSet(viewsets.ModelViewSet):
    queryset = Appliance.objects.all()
    serializer_class = ApplianceSerializer

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def update(self, request, *args, **kwargs):
        return super(ProductViewSet, self).update(request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        return super(ProductViewSet, self).partial_update(request, *args, **kwargs)


class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer

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
        }
    }
}
