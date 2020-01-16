import traceback
import json

from decimal import Decimal

from database.models import *
from rest_framework import serializers
from rest_framework.fields import empty
from rest_framework.validators import UniqueValidator

from rest_framework.utils import model_meta
from collections.abc import Mapping
from rest_framework.exceptions import ValidationError

LABEL_TRANSLATIONS = {
    "date": "Fecha",
    "name": "Nombre",
    "amount": "Cantidad",
    "unit": "Unidad",
    "plates": "Placas",
    "customer_name": "Cliente",
    "service": "Servicio",
    "discount": "Descuento",
    "authorized": "Autorizado",
    "work_sheet": "Hoja de Trabajo"
}

class DashboardListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

class DashboardSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)

    def create(self, validated_data):
        return self.Meta.model.objects.create(**validated_data)

    def update(self, instance, validated_data):
        for field, value in validated_data.items():
            setattr(instance, field, value)
        for field in instance._meta.fields:
            if field.name != 'id' and not field.name.endswith('_ptr') and not field.name in validated_data.keys():
                setattr(instance, field.name, None)
        instance.save()
        return instance

    def validate_reverse_field(self, field, serializer, parent):
        self._errors = {}
        self.reverse_fields_serializers[field] = []
        for data in json.loads(self.initial_data.get(field, "[]")):
            if 'id' in data:
                instance = serializer.Meta.model.objects.get(id=pc_data['id'])
            else:
                data[parent] = self.instance
                instance = serializer.Meta.model(**data)
            data[parent] = self.instance.id
            s = serializer(instance, data=data)
            if s.is_valid():
                self.reverse_fields_serializers[field].append(s)
            else:
                self._errors = s.errors
        if self._errors:
            raise ValidationError(self._errors)

    class Meta:
        list_serializer_class = DashboardListSerializer

class ProductListSerializer(serializers.ListSerializer):
    def create(self, validated_data):
        products = []
        for i in range(len(validated_data)):
            brand, _ = Brand.objects.get_or_create(name=self.initial_data[i].get('brandName'))
            provider, _ = Provider.objects.get_or_create(name=self.initial_data[i].get('providerName'))
            appliance, _ = Appliance.objects.get_or_create(name=self.initial_data[i].get('applianceName'))
            validated_data[i]['brand'] = brand
            validated_data[i]['provider'] = provider
            validated_data[i]['appliance'] = appliance
            products.append(Product(**validated_data[i]))
        return Product.objects.bulk_create(products)

class ProductSerializer(DashboardSerializer):
    code = serializers.CharField(validators=[UniqueValidator(queryset=Product.objects.all())])
    brand = serializers.PrimaryKeyRelatedField(queryset=Brand.objects.all(), required=False)
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all(), required=False)
    name = serializers.CharField()
    description = serializers.CharField(required=False)
    appliance = serializers.PrimaryKeyRelatedField(queryset=Appliance.objects.all(), required=False)
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    discount = serializers.DecimalField(max_digits=9, decimal_places=2)
    picture = serializers.CharField(required=False)

    def create(self, validated_data):
        brand, _ = Brand.objects.get_or_create(name=self.initial_data.get('brandName'))
        provider, _ = Provider.objects.get_or_create(name=self.initial_data.get('providerName'))
        appliance, _ = Appliance.objects.get_or_create(name=self.initial_data.get('applianceName'))
        validated_data['brand'] = brand
        validated_data['provider'] = provider
        validated_data['appliance'] = appliance
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        brand, _ = Brand.objects.get_or_create(name=self.initial_data.get('brandName'))
        provider, _ = Provider.objects.get_or_create(name=self.initial_data.get('providerName'))
        appliance, _ = Appliance.objects.get_or_create(name=self.initial_data.get('applianceName'))
        validated_data['brand'] = brand
        validated_data['provider'] = provider
        validated_data['appliance'] = appliance
        return super().update(instance, validated_data)

    class Meta:
        model = Product
        list_serializer_class = ProductListSerializer

class PercentageSerializer(DashboardSerializer):
    max_price_limit = serializers.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_1 = serializers.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_2 = serializers.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_3 = serializers.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_1 = serializers.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_2 = serializers.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_3 = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Percentage

class BrandSerializer(DashboardSerializer):
    name = serializers.CharField()

    class Meta:
        model = Brand

class ApplianceSerializer(DashboardSerializer):
    name = serializers.CharField()

    class Meta:
        model = Appliance

class EmployeeSerializer(DashboardSerializer):
    name = serializers.CharField()
    phone = serializers.CharField(required=False)

    class Meta:
        model = Employee

class ProviderSerializer(DashboardSerializer):
    name = serializers.CharField()

    class Meta:
        model = Provider

    def run_validation(self, data):
        validated_data = super().run_validation(data)
        self.validate_revese_field('provider_contact_set', ProviderContactSerializer, 'provider')
        return validated_data
    
    def update(self, instance, validated_data):
        updated_ids = []
        for pcs in self.reverse_fields_serializers['provider_contact_set']:
            pcs.save()
            updated_ids.append(pcs.instance.id)
        Provider_Contact.objects.filter(provider=instance).exclude(id__in=updated_ids).delete()
        return super().update(instance, validated_data)

class ProviderContactSerializer(DashboardSerializer):
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    name = serializers.CharField()
    department = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    for_orders = serializers.BooleanField(required=False)

    class Meta:
        model = Provider_Contact

class CustomerSerializer(DashboardSerializer):
    name = serializers.CharField()

    class Meta:
        model = Customer

    def run_validation(self, data):
        validated_data = super().run_validation(data)
        self.validate_revese_field('customer_contact_set', CustomerContactSerializer, 'customer')
        return validated_data
    
    def update(self, instance, validated_data):
        updated_ids = []
        for pcs in self.reverse_fields_serializers['customer_contact_set']:
            pcs.save()
            updated_ids.append(pcs.instance.id)
        Customer_Contact.objects.filter(customer=instance).exclude(id__in=updated_ids).delete()
        return super().update(instance, validated_data)

class CustomerContactSerializer(DashboardSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    name = serializers.CharField()
    department = serializers.CharField(required=False, allow_blank=True)
    email = serializers.EmailField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    for_quotation = serializers.BooleanField(required=False)
    for_invoice = serializers.BooleanField(required=False)

    class Meta:
        model = Customer_Contact

class OrganizationSerializer(DashboardSerializer):
    name = serializers.CharField()

    class Meta:
        model = Organization

class OrganizationStorageSerializer(DashboardSerializer):
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    storage_type = serializers.PrimaryKeyRelatedField(queryset=StorageType.objects.all(), required=False)
    storage_type_name = serializers.ReadOnlyField(source='storage_type.name')
    organization_name = serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = Organization_Storage

    def create(self, validated_data):
        storage_type, _ = StorageType.objects.get_or_create(name=self.initial_data.get('storage_type_name'))
        validated_data['storage_type'] = storage_type
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        storage_type, _ = StorageType.objects.get_or_create(name=self.initial_data.get('storage_type_name'))
        validated_data['storage_type'] = storage_type
        return super().update(instance, validated_data)

class StorageProductSerializer(DashboardSerializer):
    organization_storage = serializers.PrimaryKeyRelatedField(queryset=Organization_Storage.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField()
    must_have = serializers.IntegerField(required=False)

    class Meta:
        model = Storage_Product

class JSONSubsetSerializer(DashboardSerializer):

    def run_validation(self, data):
        if type(data) == str:
            data = json.loads(data)
        validated_data = super().run_validation(data)
        return validated_data

class MovementProductSerializer(JSONSubsetSerializer):
    movement = serializers.PrimaryKeyRelatedField(queryset=Movement_Product.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product

class MovementSerializer(DashboardSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    organization_storage = serializers.PrimaryKeyRelatedField(queryset=Organization_Storage.objects.all())
    movement_product_set = MovementProductSerializer(many=True)

    def run_validation(self, data):
        data2 = data.copy()
        if self.instance:
            self.fields['movement_product_set'].required = False
            data2["organization_storage"] = self.instance.organization_storage.id
            if not data2.get("date"):
                data2["date"] = self.instance.date
        validated_data = super().run_validation(data2)
        return validated_data

    def create(self, validated_data):
        mp_data = validated_data.pop('movement_product_set')
        obj = super().create(validated_data)
        mps = []
        for data in mp_data:
            data['movement'] = obj
            mps.append(Movement_Product(**data))
        Movement_Product.objects.bulk_create(mps)
        return obj

class OutputSerializer(MovementSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    destination = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)
    replacer = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)

    class Meta:
        model = Output


class OrderProductSerializer(JSONSubsetSerializer):
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all(), required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    amount = serializers.IntegerField()
    amount_received = serializers.IntegerField(required=False)

    class Meta:
        model = Order_Product

class OrderSerializer(DashboardSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    organization_storage = serializers.PrimaryKeyRelatedField(queryset=Organization_Storage.objects.all())
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    status = serializers.CharField(required=False)
    status_display = serializers.SerializerMethodField()
    claimant = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    replacer = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)
    received_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False, allow_null=True)
    order_product_set = OrderProductSerializer(many=True)

    class Meta:
        model = Order

    def get_status_display(self, obj):
        return obj.get_status_display()

    def run_validation(self, data):
        data2 = data.copy()
        if self.instance:
            self.fields['order_product_set'].required = False
            data2["provider"] = self.instance.provider.id
            data2["date"] = self.instance.date
            data2["status"] = self.instance.status or 'P'
            if data2.get("recieved_date"):
                data2["received_date"] = self.instance.received_date
        validated_data = super().run_validation(data2)
        return validated_data

    def create(self, validated_data):
        op_data = validated_data.pop('order_product_set')
        obj = super().create(validated_data)
        ops = []
        for data in op_data:
            data['order'] = obj
            ops.append(Order_Product(**data))
        Order_Product.objects.bulk_create(ops)
        return obj

class InputSerializer(MovementSerializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), required=False)
    invoice_number = serializers.ReadOnlyField(source='invoice.number')
    invoice_date = serializers.ReadOnlyField(source='invoice.date')

    class Meta:
        model = Input

    def create(self, validated_data):
        if self.initial_data.get('invoice_number'):
            invoice, _ = Invoice.objects.get_or_create(number=self.initial_data.get('invoice_number'), date=self.initial_data.get('invoice_date'))
            validated_data['invoice'] = invoice
        for i in range(len(validated_data['movement_product_set'])):
            data = json.loads(self.initial_data['movement_product_set'])[i]
            validated_data['movement_product_set'][i]['price'] = Decimal(float(data['price'])-(float(data['price'])*float(data['discount'])/100))
        return super().create(validated_data)

class PaymentSerializer(JSONSubsetSerializer):
    date = serializers.DateField(format="%Y-%m-%d")
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all())

    class Meta:
        model = Payment

class InvoiceSerializer(DashboardSerializer):
    date = serializers.DateField(format="%Y-%m-%d", required=False)
    number = serializers.CharField()
    provider = serializers.PrimaryKeyRelatedField(queryset=Provider.objects.all())
    due = serializers.DateField(format="%Y-%m-%d", required=False)
    paid = serializers.BooleanField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    credit = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    discount = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    payment_set = PaymentSerializer(many=True, required=False)

    class Meta:
        model = Invoice


class PriceListProductSerializer(JSONSubsetSerializer):
    pricelist = serializers.PrimaryKeyRelatedField(queryset=PriceList.objects.all(), allow_null=True, required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = PriceList_Product

class PriceListSerializer(DashboardSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all())
    pricelist_product_set = PriceListProductSerializer(many=True)

    class Meta:
        model = PriceList


class QuotationProductSerializer(JSONSubsetSerializer):
    quotation = serializers.PrimaryKeyRelatedField(queryset=Quotation.objects.all(), allow_null=True, required=False)
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Product

class QuotationOtherSerializer(JSONSubsetSerializer):
    quotation = serializers.PrimaryKeyRelatedField(queryset=Quotation.objects.all(), allow_null=True, required=False)
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Others


class QuotationSerializer(DashboardSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    pricelist = serializers.PrimaryKeyRelatedField(queryset=PriceList.objects.all(), allow_null=True, required=False)
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)
    quotation_product_set = QuotationProductSerializer(many=True)
    quotation_others_set = QuotationOtherSerializer(many=True)
    authorized = serializers.BooleanField(required=False)

    class Meta:
        model = Quotation


class CollectionSerializer(JSONSubsetSerializer):
    date = serializers.DateField()
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    sell = serializers.PrimaryKeyRelatedField(queryset=Sell.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Collection

class SellSerializer(DashboardSerializer):
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)
    paid = serializers.BooleanField(required=False)
    collection_set = CollectionSerializer(many=True)

    class Meta:
        model = Sell

class WorkSerializer(DashboardSerializer):
    date = serializers.DateField()
    start_time = serializers.TimeField(required=False)
    end_time = serializers.TimeField(required=False)
    unit_section = serializers.CharField(required=False)
    quotation = serializers.PrimaryKeyRelatedField(queryset=Quotation.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Work

class EmployeeWorkSerializer(DashboardSerializer):
    work = serializers.PrimaryKeyRelatedField(queryset=Work.objects.all(), allow_null=True, required=False)
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), allow_null=True, required=False)
    earning = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = Employee_Work