import json

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

class ShortProductSerializer(serializers.ModelSerializer):
    provider = serializers.SlugRelatedField(slug_field='name', queryset=Provider.objects.all(), allow_null=True)
    brand = serializers.SlugRelatedField(slug_field='name', queryset=Brand.objects.all(), allow_null=True)
    appliance = serializers.SlugRelatedField(slug_field='name', queryset=Appliance.objects.all(), allow_null=True)

    class Meta:
        model = Product
        fields = (
            "code",
            "name",
            "description",
            "provider",
            "name",
            "appliance"
        )

class VeryShortProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = (
            "code",
            "name",
            "description",
        )

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
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product
        exclude = (
            'movement',
            )

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product

class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    # product_code = serializers.CharField(source='product.code')
    # product_name = serializers.ReadOnlyField(source='product.name')
    # product_description = serializers.ReadOnlyField(source='product.description')
    amount = serializers.IntegerField()
    actions = serializers.SerializerMethodField()

    class Meta:
        model = Order_Product
        # fields = (
        #     'id',
        #     'product',
        #     'amount',
        #     'amount_received',
        #     'actions',
        # )
        exclude = ("order",)

    def get_actions(self, obj):
        return "Actions"

class InputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    organization = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)
    invoice = serializers.SlugRelatedField(slug_field='number', queryset=Invoice.objects.all(), allow_null=True, required=False)
    # invoice_number = serializers.SerializerMethodField()
    invoice_number = serializers.ReadOnlyField(source='invoice.number')
    invoice_date = serializers.ReadOnlyField(source='invoice.date')
    invoice_price = serializers.ReadOnlyField(source='invoice.price')
    # invoice_date = serializers.SlugRelatedField(slug_field='date', queryset=Invoice.objects.all(), allow_null=True, required=False)
    # invoice_price = serializers.SlugRelatedField(slug_field='price', queryset=Invoice.objects.all(), allow_null=True, required=False)

    class Meta:
        model = Input
        fields = (
            'id',
            'date',
            "organization_storage",
            "organization",
            'storage',
            'products',
            'invoice',
            'invoice_number',
            'invoice_date',
            'invoice_price',
        )

    def validate_products(self, value):
        value = json.loads(self.initial_data['products'])
        input_id = self.initial_data.get("id")
        if input_id:
            input_reg = Input.objects.get(id=input_id)
            for mp in value:
                mp['product'] = mp['id']
                for input_mp in input_reg.movement_product:
                    if mp['product'] == input_mp.product.id:
                        mp['id'] = input_mp.id
                        mp['status'] = 'update'
                        mp['restock'] = {
                            input_reg.organization_storage.id: -input_mp.amount,
                            self.initial_data['organization_storage']: int(mp["amount"])
                        }
                        break
                else:
                    mp['id'] = None
                    mp['status'] = 'new'
                    mp['restock'] = {self.initial_data['organization_storage']: int(mp['amount'])}
            for input_mp in input_reg.movement_product:
                for mp in value:
                    if mp['product'] == input_mp.product.id:
                        break
                else:
                    value.append({
                        'id': input_mp.id,
                        'product': input_mp.product.id,
                        'status': 'delete',
                        'restock': {input_reg.organization_storage.id: -input_mp.amount}
                    })
        else:
            for mp in value:
                mp['product'] = mp['id']
                mp['id'] = None
                mp['status'] = 'new'
                mp['restock'] = {self.initial_data['organization_storage']: int(mp['amount'])}
        return value

    # def validate_invoice_number(self, value):
    #     import pdb; pdb.set_trace()
    #     self.validate_invoice(value)
    #     return value
    #
    # def validate_invoice(self, value):
    #     import pdb; pdb.set_trace()
    #     return value

class OutputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    organization = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    products = MovementProductSerializer(source='movement_product', many=True)
    replacer_name = serializers.ReadOnlyField(source='replacer.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')
    employee_name = serializers.ReadOnlyField(source='employee.name')

    class Meta:
        model = Output
        fields = (
            'id',
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

    def validate_products(self, value):
        value = json.loads(self.initial_data['products'])
        output_id = self.initial_data.get("id")
        if output_id:
            output = Output.objects.get(id=output_id)
            for mp in value:
                mp['product'] = mp['id']
                for output_mp in output.movement_product:
                    if mp['product'] == output_mp.product.id:
                        mp['id'] = output_mp.id
                        mp['status'] = 'update'
                        mp['restock'] = {
                            output.organization_storage.id: output_mp.amount,
                            self.initial_data['organization_storage']: -int(mp["amount"])
                        }
                        break
                else:
                    mp['id'] = None
                    mp['status'] = 'new'
                    mp['restock'] = {self.initial_data['organization_storage']: -int(mp['amount'])}
            for output_mp in output.movement_product:
                for mp in value:
                    if mp['product'] == output_mp.product.id:
                        break
                else:
                    value.append({
                        'id': output_mp.id,
                        'product': output_mp.product.id,
                        'status': 'delete',
                        'restock': {output.organization_storage.id: output_mp.amount}
                    })
        else:
            for mp in value:
                mp['product'] = mp['id']
                mp['id'] = None
                mp['status'] = 'new'
                mp['restock'] = {self.initial_data['organization_storage']: -int(mp['amount'])}
        return value

class LendingSerializer(serializers.ModelSerializer):
    products = LendingProductSerializer(many=True)

    class Meta:
        model = Lending

class OrderSerializer(serializers.ModelSerializer):
    date = serializers.ReadOnlyField()
    organization = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    products = OrderProductSerializer(source='order_product', many=True)
    provider_name = serializers.ReadOnlyField(source='provider.name')
    status = serializers.SerializerMethodField()
    claimant_name = serializers.ReadOnlyField(source='claimant.name')

    class Meta:
        model = Order
        fields = (
            'id',
            'date',
            "organization_storage",
            "organization",
            'storage',
            'products',
            'provider',
            'claimant',
            'status',
            'received_date',
            'provider_name',
            'claimant_name'
        )

    def validate_products(self, value):
        value = json.loads(self.initial_data['products'])
        order_id = self.initial_data.get("id")
        if order_id:
            order = Order.objects.get(id=order_id)
            for op in value:
                op['product'] = op['id']
                for order_op in order.order_product:
                    if op['product'] == order_op.product.id:
                        op['id'] = order_op.id
                        op['status'] = 'update'
                        break
                else:
                    op['id'] = None
                    op['status'] = 'new'
            for order_op in order.order_product:
                for op in value:
                    if op['product'] == order_op.product.id:
                        break
                else:
                    value.append({
                        'id': order_op.id,
                        'product': order_op.product.id,
                        'status': 'delete',
                    })
        else:
            for op in value:
                op['product'] = op['id']
                op['id'] = None
                op['status'] = 'new'
        return value

    def get_status(self, obj):
        return obj.get_status_display()

class QuotationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quotation

class InvoiceSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%d-%B-%Y")
    due = serializers.DateTimeField(format="%d-%B-%Y")

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
