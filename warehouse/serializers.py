from warehouse.models import Provider, Brand, Appliance, Product, Organization, Input, Output, Lending, Order
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Provider
class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance

class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.StringRelatedField()
    brand = serializers.StringRelatedField()
    appliance = serializers.StringRelatedField()
    class Meta:
        model = Product

class XProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product


class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

class InputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input

class OutputSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output

class LendingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
