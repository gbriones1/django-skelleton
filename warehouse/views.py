from django.shortcuts import render
from django.shortcuts import render_to_response
from django.contrib.auth.decorators import login_required
from django.http import Http404
from django.template import RequestContext
from rest_framework import viewsets
from rest_framework.response import Response
from warehouse.models import Provider, Brand, Appliance, Product, Organization
from warehouse.forms import NewProductForm, EditProductForm
from warehouse.serializers import ProviderSerializer, BrandSerializer, ApplianceSerializer, ProductSerializer, OrganizationSerializer
from mysite import configurations
from mysite import graphics
from mysite.extensions import NotificationHandler


@login_required
def main(request, name):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = []
    scripts = ["tables"]
    if name == 'product':
        actions = graphics.Action.edit_and_delete()
        buttons = graphics.Action.new_and_multidelete()
        table = graphics.Table(
            "table-product",
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
            contents.append(modal)
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
