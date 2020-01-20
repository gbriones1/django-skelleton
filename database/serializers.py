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


class ReverseFieldReference(object):

    def __init__(self, name, model, parent, identifier):
        self.name = name
        self.model = model
        self.parent = parent
        self.identifier = identifier

class DashboardListSerializer(serializers.ListSerializer):

    def create(self, validated_data):
        return super().create(validated_data)

class DashboardSerializer(serializers.Serializer):
    id = serializers.IntegerField(required=False, read_only=True)

    def _get_reverse_field_args(self, validated_data):
        reverse_fields_args = []
        if hasattr(self.Meta, 'reverse_fields'):
            for reverse_fields_ref in self.Meta.reverse_fields:
                reverse_fields_args.append({
                    'set_data': validated_data.pop(reverse_fields_ref.name, []),
                    'reference': reverse_fields_ref
                })
        return reverse_fields_args

    def create(self, validated_data):
        reverse_fields_args = self._get_reverse_field_args(validated_data)
        instance = self.Meta.model.objects.create(**validated_data)
        for reverse_fields_arg in reverse_fields_args:
            reverse_fields_arg['instance'] = instance
            self.create_reverse_field(**reverse_fields_arg)
        return instance

    def update(self, instance, validated_data):
        reverse_fields_args = self._get_reverse_field_args(validated_data)
        for field, value in validated_data.items():
            setattr(instance, field, value)
        for field in instance._meta.fields:
            if field.name != 'id' and not field.name.endswith('_ptr') and not field.name in validated_data.keys():
                setattr(instance, field.name, None)
        instance.save()
        for reverse_fields_arg in reverse_fields_args:
            reverse_fields_arg['instance'] = instance
            self.update_reverse_field(**reverse_fields_arg)
        return instance

    def validate_reverse_field(self, field, serializer, parent):
        self._errors = {}
        if not hasattr(self, "reverse_fields_serializers"):
            self.reverse_fields_serializers = {}
        self.reverse_fields_serializers[field] = []
        for data in json.loads(self.initial_data.get(field, "[]")):
            if 'id' in data:
                instance = serializer.Meta.model.objects.get(id=data['id'])
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

    def create_reverse_field(self, set_data, instance, reference):
        obj_list = []
        for data in set_data:
            data[reference.parent] = instance
            obj_list.append(reference.model(**data))
        reference.model.objects.bulk_create(obj_list)

    def update_reverse_field(self, set_data, instance, reference):
        for obj in getattr(instance, reference.name).all():
            data = None
            if reference.identifier:
                data = next(filter(lambda x: x[reference.identifier] == getattr(obj, reference.identifier), set_data), None)
            if data:
                for field, value in data.items():
                    setattr(obj, field, value)
                obj.save()
                data[reference.parent] = instance
            else:
                obj.delete()
        obj_list = []
        for data in set_data:
            if not data.get(reference.parent):
                data[reference.parent] = instance
                obj_list.append(reference.model(**data))
        if obj_list:
            reference.model.objects.bulk_create(obj_list)

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
        self.validate_reverse_field('provider_contact_set', ProviderContactSerializer, 'provider')
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
        self.validate_reverse_field('customer_contact_set', CustomerContactSerializer, 'customer')
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

class OutputSerializer(MovementSerializer):
    employee = serializers.PrimaryKeyRelatedField(queryset=Employee.objects.all(), required=False)
    destination = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), required=False)
    replacer = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all(), required=False)

    class Meta:
        model = Output
        reverse_fields = [
            ReverseFieldReference(
                'movement_product_set',
                Movement_Product,
                'movement',
                'product'
            )
        ]


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
        reverse_fields = [
            ReverseFieldReference(
                'order_product_set',
                Order_Product,
                'order',
                'product'
            )
        ]

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

class InputSerializer(MovementSerializer):
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), required=False)
    invoice_number = serializers.ReadOnlyField(source='invoice.number')
    invoice_date = serializers.ReadOnlyField(source='invoice.date')

    class Meta:
        model = Input
        reverse_fields = [
            ReverseFieldReference(
                'movement_product_set',
                Movement_Product,
                'movement',
                'product'
            )
        ]

    def create(self, validated_data):
        if self.initial_data.get('invoice_number'):
            invoice, _ = Invoice.objects.get_or_create(number=self.initial_data.get('invoice_number'), date=self.initial_data.get('invoice_date'))
            validated_data['invoice'] = invoice
        for i in range(len(validated_data['movement_product_set'])):
            data = json.loads(self.initial_data['movement_product_set'])[i]
            validated_data['movement_product_set'][i]['price'] = Decimal(float(data['price'])-(float(data['price'])*float(data['discount'])/100))
        obj = super().create(validated_data)
        obj.invoice.recalculate_price()
        return obj

class PaymentSerializer(JSONSubsetSerializer):
    date = serializers.DateField(format="%Y-%m-%d", required=False)
    amount = serializers.DecimalField(max_digits=9, decimal_places=2)
    invoice = serializers.PrimaryKeyRelatedField(queryset=Invoice.objects.all(), required=False)

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
        reverse_fields = [
            ReverseFieldReference(
                'payment_set',
                Payment,
                'invoice',
                None
            )
        ]

    def update(self, instance, validated_data):
        obj = super().update(instance, validated_data)
        obj.recalculate_payments()
        return obj


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
        reverse_fields = [
            ReverseFieldReference(
                'pricelist_product_set',
                PriceList_Product,
                'pricelist',
                'product')
        ]


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
    quotation_product_set = QuotationProductSerializer(many=True, required=False)
    quotation_others_set = QuotationOtherSerializer(many=True, required=False)
    plates = serializers.CharField(allow_null=True, required=False)
    unit = serializers.CharField(allow_null=True, required=False)
    authorized = serializers.BooleanField(required=False)
    service = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    discount = serializers.DecimalField(max_digits=9, decimal_places=2, required=False)
    work_sheet = serializers.IntegerField(allow_null=True, required=False)

    class Meta:
        model = Quotation
        reverse_fields = [
            ReverseFieldReference(
                'quotation_product_set',
                Quotation_Product,
                'quotation',
                'product'
            ),
            ReverseFieldReference(
                'quotation_others_set',
                Quotation_Others,
                'quotation',
                None
            )
        ]

    def run_validation(self, data):
        data2 = data.copy()
        if self.instance:
            data2["date"] = self.instance.date
        validated_data = super().run_validation(data2)
        return validated_data


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