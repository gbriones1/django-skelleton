from database.models import (
    Provider, Customer, Employee, Brand, Appliance, Product, Percentage, Organization,
    StorageType, Organization_Storage, Storage_Product, PriceList, Movement_Product, Lending_Product, Order_Product,
    Movement, Input, Output, Lending, Order, Quotation, Invoice, Payment, Work, Employee_Work
)
from rest_framework import serializers


class ProviderSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()

    class Meta:
        model = Provider

    def get_product_count(self, obj):
        return len(Product.objects.filter(provider=obj))

class CustomerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand

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
    organization = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())

    class Meta:
        model = Organization_Storage

# class OrganizationStorageSerializer(serializers.ModelSerializer):
#     storage_type = serializers.SlugRelatedField(slug_field='name', queryset=StorageType.objects.all())
#     products = ProductSerializer(many=True)
#
#     class Meta:
#         model = Organization_Storage

class PriceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = PriceList

class StorageProductSerializer(serializers.ModelSerializer):
    product_code = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    product_description = serializers.ReadOnlyField()
    product_brand = serializers.ReadOnlyField()
    organization_name = serializers.ReadOnlyField()
    storage_name = serializers.ReadOnlyField()

    class Meta:
        model = Storage_Product

class MovementProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product

class OrderProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order_Product

class InputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    organization = serializers.CharField(source='organization_storage.organization.name')
    storage = serializers.CharField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)

    class Meta:
        model = Movement
        fields = ('date', 'organization', 'storage', 'products')

class OutputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField()
    organization = serializers.CharField(source='organization_storage.organization.name')
    storage = serializers.CharField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)
    replacer = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())

    class Meta:
        model = Output

class LendingSerializer(serializers.ModelSerializer):
    products = LendingProductSerializer(many=True)

    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation

class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work

class EmployeeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Work
