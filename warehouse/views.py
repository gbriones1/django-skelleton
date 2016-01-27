from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.http import Http404
from rest_framework import viewsets
from rest_framework.response import Response
from warehouse.models import Provider, Brand, Appliance, Product, Organization
from warehouse.serializers import ProviderSerializer, BrandSerializer, ApplianceSerializer, ProductSerializer, OrganizationSerializer
from mysite import configurations


@login_required
def main(request, name):
    APPNAME = configurations.APPNAME
    YEAR = configurations.YEAR
    VERSION = configurations.VERSION
    PAGE_TITLE = configurations.PAGE_TITLE
    contents = []
    if name == 'product':
        contents = ["table"]
    else:
        raise Http404("Page does not exist")
    return render_to_response('pages/warehouse.html', locals(), context_instance=RequestContext(request))

@login_required
def product(request):
    # products = ProductViewSet.as_view({'get': 'list'})(request).data
    products = ProductSerializer(Product.objects.all(), many=True).data
    return render_to_response('pages/dashboard.html', locals(), context_instance=RequestContext(request))

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

class OrganizationViewSet(viewsets.ModelViewSet):
    queryset = Organization.objects.all()
    serializer_class = OrganizationSerializer
