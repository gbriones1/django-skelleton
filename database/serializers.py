from database.models import (
    Provider, Provider_Contact, Contact, Customer, Employee, Brand, Appliance, Product, Percentage, Organization,
    StorageType, Organization_Storage, Storage_Product, PriceList, Movement_Product, Lending_Product, Order_Product,
    Movement, Input, Output, Lending, Order, Quotation, Invoice, Payment, Work, Employee_Work
)
from rest_framework import serializers

class ProviderContactSerializer(serializers.ModelSerializer):
    # Nombre = serializers.SlugRelatedField(source='contact', slug_field='name', queryset=Contact.objects.all(), allow_null=True)
    Nombre = serializers.CharField(source='contact.name')
    Departamento = serializers.CharField(source='contact.department')
    Telefono = serializers.CharField(source='contact.phone')
    Email = serializers.CharField(source='contact.email')
    Pedidos = serializers.SerializerMethodField('get_for_orders_value')

    class Meta:
        model = Provider_Contact
        exclude = (
            'id',
            'provider',
            'contact',
            'for_orders'
        )

    def get_for_orders_value(self, obj):
        if obj.for_orders:
            return "Si"
        return "No"

class ProviderSerializer(serializers.ModelSerializer):
    product_count = serializers.SerializerMethodField()
    contacts = ProviderContactSerializer(source='provider_contact', many=True)

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
    # storage_type = serializers.SlugRelatedField(slug_field='name', queryset=StorageType.objects.all())
    # organization = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())
    storage_type = serializers.CharField(source='storage_type.name')
    organization = serializers.CharField(source='organization.name')

    class Meta:
        model = Organization_Storage

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
    # product = ProductSerializer()
    # product = serializers.SlugRelatedField(slug_field='name', queryset=Product.objects.all())
    id = serializers.ReadOnlyField(source='product.id')
    product_code = serializers.CharField(source='product.code')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_description = serializers.ReadOnlyField(source='product.description')
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product
        exclude = ('movement','product')

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product

class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product_code = serializers.CharField(source='product.code')
    product_name = serializers.ReadOnlyField(source='product.name')
    product_description = serializers.ReadOnlyField(source='product.description')
    amount = serializers.IntegerField()

    class Meta:
        model = Order_Product
        exclude = ('order','product')

class InputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%B-%Y")
    organization = serializers.CharField(source='organization_storage.organization.name')
    storage = serializers.CharField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)
    invoice_number = serializers.ReadOnlyField(source='invoice.number')

    class Meta:
        model = Input
        fields = (
            'date',
            "organization_storage",
            "organization",
            'storage',
            'products',
            'invoice',
            'invoice_number',
        )

class OutputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%B-%Y")
    organization = serializers.CharField(source='organization_storage.organization.name')
    storage = serializers.CharField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)
    replacer_name = serializers.ReadOnlyField(source='replacer.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')
    employee_name = serializers.ReadOnlyField(source='employee.name')

    class Meta:
        model = Output
        fields = (
            'date',
            "organization_storage",
            "organization",
            'storage',
            'products',
            'replacer',
            'destination',
            'employee',
            'replacer_name',
            'destination_name',
            'employee_name'
        )

class LendingSerializer(serializers.ModelSerializer):
    products = LendingProductSerializer(many=True)

    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%B-%Y")
    organization = serializers.CharField(source='organization_storage.organization.name')
    storage = serializers.CharField(source='organization_storage.storage_type.name')
    products = OrderProductSerializer(source='order_product', many=True)
    claimant_name = serializers.ReadOnlyField(source='claimant.name')

    class Meta:
        model = Order
        fields = (
            'date',
            "organization_storage",
            "organization",
            'storage',
            'products',
            'claimant',
            'claimant_name'
        )

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
