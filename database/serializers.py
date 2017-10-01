import json

from database.models import *
from rest_framework import serializers

class CheckboxField(serializers.BooleanField):

    def run_validation(self, data=serializers.empty):
        true_values = ["on", "Si"]
        if data in true_values:
            data=True
        else:
            data=False
        return super(CheckboxField, self).run_validation(data)

class ContactSerializer(serializers.ModelSerializer):

    class Meta:
        model = Contact
        fields = '__all__'

class ProviderContactSerializer(serializers.ModelSerializer):
    name = serializers.CharField(source='contact.name')
    department = serializers.CharField(source='contact.department')
    phone = serializers.CharField(source='contact.phone')
    email = serializers.CharField(source='contact.email')
    for_orders = serializers.SerializerMethodField('get_for_orders_value')

    class Meta:
        model = Provider_Contact
        exclude = (
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
    contacts = ContactSerializer(many=True)

    class Meta:
        model = Provider
        fields = '__all__'

    def get_product_count(self, obj):
        return len(Product.objects.filter(provider=obj))

    def validate_contacts(self, value):
        value = json.loads(self.initial_data.get('contacts', '[]') or '[]')
        for c in value:
            c['status'] = 'new'
        provider_id = self.initial_data.get("id")
        if provider_id:
            provider = Provider.objects.get(id=provider_id)
            for contact in provider.provider_contact:
                for c in value:
                    if c.get('id') == contact.id:
                        c['status'] = 'update'
                        break
                else:
                    value.append({
                        'id': contact.id,
                        'status': 'delete',
                    })
        return value

class CustomerSerializer(serializers.ModelSerializer):
    contacts = ContactSerializer(source='customer_contact', many=True)

    class Meta:
        model = Customer
        fields = '__all__'

    def validate_contacts(self, value):
        value = json.loads(self.initial_data.get('contacts', '[]') or '[]')
        for c in value:
            c['status'] = 'new'
        customer_id = self.initial_data.get("id")
        if customer_id:
            customer = Customer.objects.get(id=customer_id)
            for contact in customer.contacts.all():
                for c in value:
                    if c.get('id') == contact.id:
                        c['status'] = 'update'
                        break
                else:
                    value.append({
                        'id': contact.id,
                        'status': 'delete',
                    })
        return value

class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'

class ApplianceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appliance
        fields = '__all__'

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
        fields = '__all__'

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
        fields = '__all__'

class OrganizationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationStorageSerializer(serializers.ModelSerializer):
    # storage_type = serializers.SlugRelatedField(slug_field='name', queryset=StorageType.objects.all())
    # organization = serializers.SlugRelatedField(slug_field='name', queryset=Organization.objects.all())
    storage_type = serializers.CharField(source='storage_type.name')
    organization = serializers.CharField(source='organization.name')

    class Meta:
        model = Organization_Storage
        fields = '__all__'

class PriceListProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = PriceList_Product
        exclude = (
            'pricelist',
            )

class PriceListSerializer(serializers.ModelSerializer):
    # customer = serializers.SlugRelatedField(slug_field='name', queryset=Customer.objects.all(), required=False)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    products = PriceListProductSerializer(source='pricelist_product', many=True)

    class Meta:
        model = PriceList
        fields = (
            'id',
            'customer',
            'products',
            'customer_name'
        )

    def validate_products(self, value):
        value = json.loads(self.initial_data['products'])
        pricelist_id = self.initial_data.get("id")
        if pricelist_id:
            pricelist = PriceList.objects.get(id=pricelist_id)
            for pp in value:
                pp['product'] = pp['id']
                for pricelist_pp in pricelist.pricelist_product:
                    if pp['product'] == pricelist_pp.product.id:
                        pp['id'] = pricelist_pp.id
                        pp['status'] = 'update'
                        break
                else:
                    pp['id'] = None
                    pp['status'] = 'new'
            for pricelist_pp in pricelist.pricelist_product:
                for pp in value:
                    if pp['product'] == pricelist_pp.product.id:
                        break
                else:
                    value.append({
                        'id': pricelist_pp.id,
                        'product': pricelist_pp.product.id,
                        'status': 'delete',
                    })
        else:
            for pp in value:
                pp['product'] = pp['id']
                pp['id'] = None
                pp['status'] = 'new'
        return value

class StorageProductSerializer(serializers.ModelSerializer):
    product_code = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    product_description = serializers.ReadOnlyField()
    product_brand = serializers.ReadOnlyField()
    organization_name = serializers.ReadOnlyField()
    storage_name = serializers.ReadOnlyField()

    class Meta:
        model = Storage_Product
        fields = '__all__'

class MovementProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    real_price = serializers.DecimalField(max_digits=9, decimal_places=2, source='price')
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product
        exclude = (
            'movement',
            )

class InputProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    price = serializers.ReadOnlyField(source='product.price')
    discount = serializers.ReadOnlyField(source='product.discount')
    real_price = serializers.DecimalField(max_digits=9, decimal_places=2, source='price')
    amount = serializers.IntegerField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Movement_Product
        exclude = (
            'movement',
            )

    def get_total_price(self, obj):
        return obj.price * obj.amount

class OutputProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()
    total_price = serializers.SerializerMethodField()

    class Meta:
        model = Movement_Product
        exclude = (
            'movement',
            )

    def get_total_price(self, obj):
        return obj.price * obj.amount

class LendingProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lending_Product
        fields = '__all__'

class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    # product_code = serializers.CharField(source='product.code')
    # product_name = serializers.ReadOnlyField(source='product.name')
    # product_description = serializers.ReadOnlyField(source='product.description')
    amount = serializers.IntegerField()
    price = serializers.ReadOnlyField(source='product.price')
    discount = serializers.ReadOnlyField(source='product.discount')
    # actions = serializers.SerializerMethodField()

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
    products = InputProductSerializer(source='movement_product', many=True)
    invoice = serializers.SlugRelatedField(slug_field='id', queryset=Invoice.objects.all(), allow_null=True, required=False)
    # invoice = serializers.SlugRelatedField(slug_field='number', queryset=Invoice.objects.all(), allow_null=True, required=False)
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
        for mp in value:
            product = Product.objects.get(id=mp['product'])
            product.price = float(mp['price'])
            product.discount = float(mp['discount'])
            product.save()
            mp['price'] = str(product.price - (product.price*product.discount/100))
        return value

    def validate_invoice(self, value):
        if not value:
            invoice_number = self.initial_data.get("invoice_number")
            invoice_date = self.initial_data.get("invoice_date")
            if invoice_number and invoice_date:
                value = Invoice.objects.get(number=invoice_number, date=invoice_date)
        return value

class OutputSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")
    organization = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    products = OutputProductSerializer(source='movement_product', many=True)
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
        fields = '__all__'

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

class QuotationProductSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(source='product.id')
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Product
        exclude = (
            'quotation',
            )

class QuotationOtherSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Others
        exclude = (
            'quotation',
            )

class QuotationSerializer(serializers.ModelSerializer):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    pricelist = serializers.PrimaryKeyRelatedField(queryset=PriceList.objects.all(), allow_null=True, required=False)
    pricelist_name = serializers.ReadOnlyField(source='pricelist.customer.name')
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    # customer = serializers.ReadOnlyField(source='pricelist.customer.id')
    products = QuotationProductSerializer(source='quotation_product', many=True)
    others = QuotationOtherSerializer(source='quotation_other', many=True)
    authorized = CheckboxField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Quotation
        fields = (
            "id",
            "date",
            "pricelist",
            "unit",
            "plates",
            "authorized",
            "products",
            "others",
            "service",
            "discount",
            "customer",
            "pricelist_name",
            "customer_name",
            "total",
        )

    def get_total(self, obj):
        price = 0.0
        for quotation_product in obj.quotation_product:
            price += float(quotation_product.price)*quotation_product.amount
        for quotation_other in obj.quotation_other:
            price += float(quotation_other.price)*quotation_other.amount
        price += float(obj.service)
        price -= float(obj.discount)
        return price

    def validate_products(self, value):
        value = json.loads(self.initial_data['products'])
        quotation_id = self.initial_data.get("id")
        if quotation_id:
            quotation = Quotation.objects.get(id=quotation_id)
            for qp in value:
                qp['product'] = qp['id']
                for quotation_qp in quotation.quotation_product:
                    if qp['product'] == quotation_qp.product.id:
                        qp['id'] = quotation_qp.id
                        qp['status'] = 'update'
                        break
                else:
                    qp['id'] = None
                    qp['status'] = 'new'
            for quotation_qp in quotation.quotation_product:
                for qp in value:
                    if qp['product'] == quotation_qp.product.id:
                        break
                else:
                    value.append({
                        'id': quotation_qp.id,
                        'product': quotation_qp.product.id,
                        'status': 'delete',
                    })
        else:
            for qp in value:
                qp['product'] = qp['id']
                qp['id'] = None
                qp['status'] = 'new'
        pricelist = self.initial_data.get('pricelist')
        if pricelist:
            pricelist = PriceList.objects.get(id=pricelist)
            for qp in value:
                for pricelist_pp in pricelist.pricelist_product:
                    if pricelist_pp.product.id == qp['product']:
                        qp['price'] = pricelist_pp.price
                        break
        return value

    def validate_others(self, value):
        others = self.initial_data.get('others')
        value = json.loads(others) if others else []
        quotation_id = self.initial_data.get("id")
        if quotation_id:
            quotation = Quotation.objects.get(id=quotation_id)
            for qo in value:
                for quotation_qo in quotation.quotation_other:
                    if qo['id'] == quotation_qo.id:
                        qo['status'] = 'update'
                        break
                else:
                    qo['id'] = None
                    qo['status'] = 'new'
            for quotation_qo in quotation.quotation_other:
                for qo in value:
                    if qo['id'] == quotation_qo.id:
                        break
                else:
                    value.append({
                        'id': quotation_qo.id,
                        'status': 'delete',
                    })
        else:
            for qo in value:
                qo['id'] = None
                qo['status'] = 'new'
        return value

    def validate_customer(self, value):
        if self.initial_data["pricelist"]:
            value = PriceList.objects.get(id=self.initial_data["pricelist"]).customer
        return value

class InvoiceSerializer(serializers.ModelSerializer):
    provider_name = serializers.ReadOnlyField(source='provider.name')
    paid = CheckboxField()

    class Meta:
        model = Invoice
        fields = '__all__'

class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'

class SellSerializer(serializers.ModelSerializer):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    paid = CheckboxField()

    class Meta:
        model = Sell
        fields = '__all__'

class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = '__all__'

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = '__all__'

class EmployeeWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Employee_Work
        fields = '__all__'
