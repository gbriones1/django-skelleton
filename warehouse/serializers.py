from warehouse.models import Provider, Brand, Appliance, Product, Percentage, StorageType, Storage_Product, Organization, Organization_Storage, Movement, Input, Output, Lending, Order, Input_Product, Output_Product, Lending_Product, Order_Product
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
    real_price = serializers.ReadOnlyField()
    percentage_1 = serializers.ReadOnlyField()
    percentage_2 = serializers.ReadOnlyField()
    percentage_3 = serializers.ReadOnlyField()

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

class StorageProductSerializer(serializers.ModelSerializer):
    product_code = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    product_description = serializers.ReadOnlyField()
    product_brand = serializers.ReadOnlyField()
    organization_name = serializers.ReadOnlyField()
    storage_name = serializers.ReadOnlyField()

    class Meta:
        model = Storage_Product

class InputProductSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='product.code')
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    brand = serializers.CharField(source='product.brand.name')

    class Meta:
        model = Input_Product
        exclude = ("id", "input_reg", "product")

class OutputProductSerializer(serializers.ModelSerializer):
    code = serializers.CharField(source='product.code')
    name = serializers.CharField(source='product.name')
    description = serializers.CharField(source='product.description')
    brand = serializers.CharField(source='product.brand.name')

    class Meta:
        model = Output_Product
        exclude = ("id", "output_reg", "product")

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Product

class InputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='movement.date')
    organization = serializers.CharField(source='movement.organization_storage.organization.name')
    storage = serializers.CharField(source='movement.organization_storage.storage_type.name')
    input_product_set = InputProductSerializer(many=True)

    class Meta:
        model = Input
        exclude = ('movement',)

class OutputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(source='movement.date')
    organization = serializers.CharField(source='movement.organization_storage.organization.name')
    storage = serializers.CharField(source='movement.organization_storage.storage_type.name')
    output_product_set = OutputProductSerializer(many=True)
    replacer = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())

    class Meta:
        model = Output
        exclude = ('movement',)

class LendingSerializer(serializers.ModelSerializer):
    movement = MovementSerializer()
    lendings = LendingProductSerializer(many=True)

    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
