from warehouse.models import Provider, Brand, Appliance, Product, Percentage, StorageType, Organization, Organization_Storage, Movement, Input, Output, Lending, Order, Input_Product, Output_Product, Lending_Product, Order_Product
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Provider

    def get_product_count(self, obj):
        return len(Product.objects.filter(provider=obj))

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance

class ProductSerializer(serializers.ModelSerializer):
    provider = serializers.SlugRelatedField(slug_field='name', queryset=Provider.objects.all(), allow_null=True)
    brand = serializers.SlugRelatedField(slug_field='name', queryset=Brand.objects.all(), allow_null=True)
    appliance = serializers.SlugRelatedField(slug_field='name', queryset=Appliance.objects.all(), allow_null=True)

    class Meta:
        model = Product

class PercentageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Percentage

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization

class OrganizationStorageSerializer(serializers.ModelSerializer):
    storage_type = serializers.SlugRelatedField(slug_field='name', queryset=StorageType.objects.all())
    products = ProductSerializer(many=True)

    class Meta:
        model = Organization_Storage

class MovementSerializer(serializers.ModelSerializer):
    organization_storage = OrganizationStorageSerializer()

    class Meta:
        model = Movement

class InputProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Input_Product

class OutputProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Output_Product

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Product

class InputSerializer(serializers.ModelSerializer):
    movement = MovementSerializer()
    inputs = InputProductSerializer(many=True)

    class Meta:
        model = Input

class OutputSerializer(serializers.ModelSerializer):
    movement = MovementSerializer()
    outputs = OutputProductSerializer(many=True)
    replacer = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())

    class Meta:
        model = Output

class LendingSerializer(serializers.ModelSerializer):
    movement = MovementSerializer()
    lendings = LendingProductSerializer(many=True)

    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
