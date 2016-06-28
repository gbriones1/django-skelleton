from warehouse.models import Provider, Brand, Appliance, Product, Organization, Storage_Product
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

class StorageProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage_Product
