import traceback
import json

from decimal import Decimal

from database.models import *
from rest_framework import serializers
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

class SerializerListWrapper(serializers.ListSerializer):

    def to_internal_value(self, data):
        try:
            obj = []
            for mp in json.loads(data):
                obj.append(self.child.to_internal_value(mp))
            return obj
        except (TypeError, ValueError):
            self.fail('invalid')

    def run_validation(self, data):
        data_list = super(SerializerListWrapper, self).run_validation(data)
        validated_list = []
        for validated in data_list:
            validated_list.append(self.child.Meta.model(**dict(validated)))
        return validated_list

class SerializerWrapper(serializers.ModelSerializer):

    class Meta:
        list_serializer_class = SerializerListWrapper

    def run_validation(self, data):
        if 'id' in data:
            updated = self.__class__(self.instance).data
            updated.update(data)
            data = updated
        validated = super(SerializerWrapper, self).run_validation(data)
        return validated

    @classmethod
    def select_fields(cls, selected=None):
        result = []
        fields = cls.get_fields_desc()
        if selected is None:
            return fields.values()
        else:
            for name in selected:
                result.append(fields[name])
        return result

    @classmethod
    def get_fields_desc(cls):
        translations = LABEL_TRANSLATIONS
        translations.update(getattr(cls.Meta, "translations", {}))
        fields_desc = {}
        for name, field in model_meta.get_field_info(cls.Meta.model).fields.items():
            fields_desc[name] = {
                'name': name,
                'type': field.__class__.__name__,
                'label': translations.get(name, field.formfield().label),
            }
        for name, field in model_meta.get_field_info(cls.Meta.model).forward_relations.items():
            fields_desc[name] = {
                'name': name,
                'type': field.model_field.__class__.__name__,
                'label': translations.get(name, field.model_field.formfield().label),
            }
        for name, field in model_meta.get_field_info(cls.Meta.model).reverse_relations.items():
            fields_desc[name] = {
                'name': name,
                'type': "ReverseRelation",
                'label': translations.get(name, field.related_model.__name__),
                'model': field.related_model.__name__
            }
        for name, field in cls().fields.items():
            fields_desc[name] = {
                'name': name,
                'type': field.__class__.__name__,
                'label': translations.get(name, field.label),
            }
            if field.__class__.__name__ == "ListSerializer":
                fields_desc[name]['serializer'] = field.child.__class__
        return fields_desc

    def validate_reverse_field(self, value, model, field_name):
        result = []
        value = json.loads(self.initial_data.get(field_name, '[]') or '[]')
        for desc in value:
            extra_fields = {}
            for field in desc.keys():
                try:
                    field_type = model._meta.get_field(field)
                    if field_type and field_type.__class__.__name__ == "ForeignKey":
                        desc[field] = model._meta.get_field(field).related_model.objects.get(id=desc[field])
                    elif field_type and field_type.__class__.__name__ == "BooleanField":
                        desc[field] = True if desc[field] == "Si" else False
                except:
                    extra_fields[field] = desc[field]
            for field in extra_fields.keys():
                desc.pop(field)
            desc_id = desc.get("id")
            if desc_id == "undefined":
                desc.pop("id")
                desc_id = None
            if desc_id:
                instance = model.objects.get(id=desc_id)
                for field, value in desc.items():
                    setattr(instance, field, value)
            else:
                instance = model(**desc)
            for field in extra_fields.keys():
                setattr(instance, field, extra_fields[field])
            result.append(instance)
        return result

    def to_internal_value(self, data):
        if not isinstance(data, Mapping):
            try:
                if type(data) == int:
                    new_data = {}
                    instance = self.Meta.model.objects.get(id=data)
                    for field in self.data.keys():
                        new_data[field] = instance.serializable_value(field)
                    data = new_data
                else:
                    data = json.loads(data)
            except:
                pass
        for key, value in data.items():
            if key.endswith("_set") and isinstance(value, str) and value.startswith("[") and value.endswith("]"):
                try:
                    data[key] = json.loads(value)
                except:
                    pass
        return super(SerializerWrapper, self).to_internal_value(data)

    def create(self, validated_data):
        ModelClass = self.Meta.model
        info = model_meta.get_field_info(ModelClass)
        many_to_many = {}
        for field_name, relation_info in info.forward_relations.items():
            if relation_info.to_many and (field_name in validated_data):
                many_to_many[field_name] = validated_data.pop(field_name)
            else:
                obj = validated_data.get(field_name)
                if obj and isinstance(obj, relation_info.related_model):
                    obj.save()
        reverse_items = {}
        for field_name, relation_info in info.reverse_relations.items():
            if relation_info.to_many and (field_name in validated_data):
                for field in relation_info.related_model._meta.fields:
                    if field.related_model == self.Meta.model or field.related_model in self.Meta.model.__bases__:
                        reverse_items[field_name] = {"objects": validated_data.pop(field_name), "related_field":field.name}
                        break
        try:
            # print(validated_data)
            instance = ModelClass.objects.create(**validated_data)
        except TypeError:
            tb = traceback.format_exc()
            msg = (
                'Got a `TypeError` when calling `%s.objects.create()`. '
                'This may be because you have a writable field on the '
                'serializer class that is not a valid argument to '
                '`%s.objects.create()`. You may need to make the field '
                'read-only, or override the %s.create() method to handle '
                'this correctly.\nOriginal exception was:\n %s' %
                (
                    ModelClass.__name__,
                    ModelClass.__name__,
                    self.__class__.__name__,
                    tb
                )
            )
            raise TypeError(msg)

        if many_to_many:
            for field_name, value in many_to_many.items():
                field = getattr(instance, field_name)
                field.set(value)
        if reverse_items:
            for field_name, value in reverse_items.items():
                for obj in value["objects"]:
                    setattr(obj, value["related_field"], instance)
                    obj.save()
                    # instance.movement_product_set.add(obj)
        return instance



    def update(self, instance, validated_data):
        info = model_meta.get_field_info(instance)
        reverse_items = {}
        for attr, value in list(validated_data.items()):
            if attr in info.forward_relations and info.relations[attr].to_many:
                field = getattr(instance, attr)
                field.set(value)
            elif attr in info.reverse_relations and info.relations[attr].to_many:
                for field in info.reverse_relations.get(attr).related_model._meta.fields:
                    if field.related_model == self.Meta.model or field.related_model in self.Meta.model.__bases__:
                        reverse_items[attr] = {"objects": validated_data.pop(attr), "related_field":field.name}
                        break
            else:
                setattr(instance, attr, value)
        instance.save()
        if reverse_items:
            for field_name, value in reverse_items.items():
                old_items = getattr(instance, field_name).exclude(id__in=[x.id for x in value["objects"] if x.id])
                for obj in old_items:
                    obj.delete()
                for obj in value["objects"]:
                    if not obj.id:
                        setattr(obj, value["related_field"], instance)
                    obj.save()
        return instance

class CheckboxField(serializers.BooleanField):

    def run_validation(self, data=serializers.empty):
        if data in ["on", "Si"]:
            data = True
        else:
            data = False
        return super(CheckboxField, self).run_validation(data)

    def get_value(self, data):
        return super(CheckboxField, self).get_value(data)

class ProviderContactSerializer(SerializerWrapper):
    name = serializers.CharField()
    department = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    for_orders = CheckboxField()
    provider = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Provider_Contact
        fields = '__all__'

    def run_validation(self, data):
        validated = super(ProviderContactSerializer, self).run_validation(data)
        if 'id' in validated:
            return self.Meta.model.objects.get(id=validated['id'])
        return self.Meta.model(**dict(validated))

class ProviderSerializer(SerializerWrapper):
    product_count = serializers.SerializerMethodField()
    provider_contact_set = ProviderContactSerializer(many=True, required=False)

    class Meta:
        model = Provider
        fields = '__all__'

    def get_product_count(self, obj):
        return obj.product_set.count()

class CustomerContactSerializer(SerializerWrapper):
    name = serializers.CharField()
    department = serializers.CharField(allow_blank=True, required=False)
    phone = serializers.CharField(allow_blank=True, required=False)
    email = serializers.CharField(allow_blank=True, required=False)
    for_quotation = CheckboxField()
    customer = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Customer_Contact
        fields = '__all__'

    def run_validation(self, data):
        validated = super(CustomerContactSerializer, self).run_validation(data)
        if 'id' in validated:
            return self.Meta.model.objects.get(id=validated['id'])
        return self.Meta.model(**dict(validated))

class CustomerSerializer(SerializerWrapper):
    customer_contact_set = CustomerContactSerializer(many=True, required=False)

    class Meta:
        model = Customer
        fields = '__all__'

class EmployeeSerializer(SerializerWrapper):
    class Meta:
        model = Employee
        fields = '__all__'

class BrandSerializer(SerializerWrapper):
    product_amount = serializers.SerializerMethodField()

    class Meta:
        model = Brand
        fields = '__all__'

    def get_product_amount(self, obj):
        return obj.product_set.count()

class ApplianceSerializer(SerializerWrapper):
    product_amount = serializers.SerializerMethodField()

    class Meta:
        model = Appliance
        fields = '__all__'

    def get_product_amount(self, obj):
        return obj.product_set.count()

class MultiSlugRelatedField(serializers.SlugRelatedField):
    def __init__(self, fields=[], *args, **kwargs):
        self.filter_fields = fields
        super(MultiSlugRelatedField, self).__init__(*args, **kwargs)

    def to_internal_value(self, data):
        try:
            filters = {self.slug_field: data}
            for field_name in self.filter_fields:
                filters[self.parent.fields[field_name].source.split(".")[1]] = self.parent.initial_data["invoice_date"]
            return {self.field_name: filters}
        except (TypeError, ValueError):
            self.fail('invalid')

    def run_validation(self, data):
        validated = super(MultiSlugRelatedField, self).run_validation(data)
        if validated is None:
            return validated
        query = self.get_queryset().filter(**validated[self.field_name])
        if len(query):
            return query[0]
        return self.get_queryset().model(**validated[self.field_name])

class ProductSerializer(SerializerWrapper):
    provider_name = serializers.ReadOnlyField(source='provider.name')
    brand_name = serializers.ReadOnlyField(source='brand.name')
    appliance_name = serializers.ReadOnlyField(source='appliance.name')
    provider = MultiSlugRelatedField(slug_field='name', queryset=Provider.objects.all(), allow_null=True)
    brand = MultiSlugRelatedField(slug_field='name', queryset=Brand.objects.all(), allow_null=True)
    appliance = MultiSlugRelatedField(slug_field='name', queryset=Appliance.objects.all(), allow_null=True)
    picture = serializers.ImageField(required=False, allow_null=True)
    real_price = serializers.ReadOnlyField()
    percentage_1 = serializers.ReadOnlyField()
    percentage_2 = serializers.ReadOnlyField()
    percentage_3 = serializers.ReadOnlyField()

    class Meta:
        model = Product
        fields = '__all__'

class ShortProductSerializer(SerializerWrapper):
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

class VeryShortProductSerializer(SerializerWrapper):
    code = serializers.CharField(read_only=True)
    name = serializers.CharField(read_only=True)
    description = serializers.CharField(read_only=True)

    def run_validation(self, data):
        try:
            return self.Meta.model.objects.get(id=data)
        except:
            raise ValidationError(detail={"key":"value"})

    class Meta:
        model = Product
        fields = (
            "id",
            "code",
            "name",
            "description",
        )

class PercentageSerializer(SerializerWrapper):
    class Meta:
        model = Percentage
        fields = '__all__'

class OrganizationSerializer(SerializerWrapper):
    class Meta:
        model = Organization
        fields = '__all__'

class OrganizationStorageSerializer(SerializerWrapper):
    storage_type = MultiSlugRelatedField(slug_field='name', queryset=StorageType.objects.all())
    organization = serializers.PrimaryKeyRelatedField(queryset=Organization.objects.all())
    storage_type_name = serializers.ReadOnlyField(source='storage_type.name')
    organization_name = serializers.ReadOnlyField(source='organization.name')

    class Meta:
        model = Organization_Storage
        fields = '__all__'

class PriceListProductSerializer(SerializerWrapper):
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        model = PriceList_Product
        fields = '__all__'

class PriceListSerializer(SerializerWrapper):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    pricelist_product_set = PriceListProductSerializer(many=True)

    class Meta:
        model = PriceList
        fields = '__all__'

    def validate_pricelist_product_set(self, value):
        return self.validate_reverse_field(value, PriceList_Product, "pricelist_product_set")

class StorageProductSerializer(SerializerWrapper):
    product_code = serializers.ReadOnlyField()
    product_name = serializers.ReadOnlyField()
    product_description = serializers.ReadOnlyField()
    product_brand = serializers.ReadOnlyField()
    organization_name = serializers.ReadOnlyField()
    storage_name = serializers.ReadOnlyField()

    class Meta:
        model = Storage_Product
        fields = '__all__'


class LendingProductSerializer(SerializerWrapper):
    class Meta:
        model = Lending_Product
        fields = '__all__'

class OrderProductSerializer(SerializerWrapper):
    id = serializers.ReadOnlyField()
    product = VeryShortProductSerializer()
    amount = serializers.IntegerField()

    class Meta:
        model = Order_Product
        fields = '__all__'

    def run_validation(self, data):
        validated = super(OrderProductSerializer, self).run_validation(data)
        if 'id' in validated:
            return self.Meta.model.objects.get(id=validated['id'])
        return self.Meta.model(**dict(validated))

class MovementProductSerializer(SerializerWrapper):
    id = serializers.ReadOnlyField()
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Movement_Product
        exclude = (
            'movement',
            )

    def get_total_price(self, obj):
        return obj.price * obj.amount

    def run_validation(self, data):
        validated = super(MovementProductSerializer, self).run_validation(data)
        if 'id' in validated:
            return self.Meta.model.objects.get(id=validated['id'])
        return self.Meta.model(**dict(validated))


class InputSerializer(SerializerWrapper):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    organization_name = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage_name = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    movement_product_set = MovementProductSerializer(many=True)
    invoice = MultiSlugRelatedField(fields=["invoice_date"], slug_field="number", queryset=Invoice.objects.all())
    invoice_number = serializers.ReadOnlyField(source='invoice.number')
    invoice_date = serializers.ReadOnlyField(source='invoice.date')
    invoice_price = serializers.ReadOnlyField(source='invoice.price')

    class Meta:
        model = Input
        fields = '__all__'

    def validate_movement_product_set(self, value):
        for mp_data in self.initial_data['movement_product_set']:
            found = False
            for obj in value:
                if obj.product.id == int(mp_data['product']):
                    obj.discount = mp_data['discount']
                    break
        return value

class OutputSerializer(SerializerWrapper):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    organization_name = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage_name = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    movement_product_set = MovementProductSerializer(many=True)
    replacer_name = serializers.ReadOnlyField(source='replacer.name')
    destination_name = serializers.ReadOnlyField(source='destination.name')
    employee_name = serializers.ReadOnlyField(source='employee.name')

    class Meta:
        model = Output
        fields = '__all__'

class LendingSerializer(SerializerWrapper):
    organization_name = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage_name = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    products = LendingProductSerializer(many=True)

    class Meta:
        model = Lending
        fields = '__all__'

class OrderSerializer(SerializerWrapper):
    date = serializers.ReadOnlyField()
    organization_name = serializers.ReadOnlyField(source='organization_storage.organization.name')
    storage_name = serializers.ReadOnlyField(source='organization_storage.storage_type.name')
    order_product_set = OrderProductSerializer(many=True)
    provider_name = serializers.ReadOnlyField(source='provider.name')
    status = serializers.SerializerMethodField()
    claimant_name = serializers.ReadOnlyField(source='claimant.name')
    replacer_name = serializers.ReadOnlyField(source='replacer.name')

    class Meta:
        model = Order
        fields = '__all__'

    def get_status(self, obj):
        return obj.get_status_display()

class QuotationProductSerializer(SerializerWrapper):
    id = serializers.ReadOnlyField()
    product = VeryShortProductSerializer()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Product
        exclude = (
            'quotation',
            )

class QuotationOtherSerializer(SerializerWrapper):
    id = serializers.ReadOnlyField()
    description = serializers.CharField()
    price = serializers.DecimalField(max_digits=9, decimal_places=2)
    amount = serializers.IntegerField()

    class Meta:
        model = Quotation_Others
        exclude = (
            'quotation',
            )


class QuotationSerializer(SerializerWrapper):
    date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S", required=False)
    pricelist = serializers.PrimaryKeyRelatedField(queryset=PriceList.objects.all(), allow_null=True, required=False)
    pricelist_name = serializers.ReadOnlyField(source='pricelist.customer.name')
    customer = serializers.PrimaryKeyRelatedField(queryset=Customer.objects.all(), allow_null=True, required=False)
    customer_name = serializers.ReadOnlyField(source='customer.name')
    quotation_product_set = QuotationProductSerializer(many=True)
    quotation_others_set = QuotationOtherSerializer(many=True)
    authorized = CheckboxField()
    total = serializers.SerializerMethodField()

    class Meta:
        model = Quotation
        fields = "__all__"

    def get_total(self, obj):
        price = 0.0
        for quotation_product in obj.quotation_product_set.all():
            price += float(quotation_product.price)*quotation_product.amount
        for quotation_other in obj.quotation_others_set.all():
            price += float(quotation_other.price)*quotation_other.amount
        price += float(obj.service)
        price -= float(obj.discount)
        return price

    def validate_quotation_product_set(self, value):
        return self.validate_reverse_field(value, Quotation_Product, "quotation_product_set")

    def validate_quotation_others_set(self, value):
        return self.validate_reverse_field(value, Quotation_Others, "quotation_others_set")

    def validate_customer(self, value):
        if self.initial_data["pricelist"]:
            value = PriceList.objects.get(id=self.initial_data["pricelist"]).customer
        return value

class PaymentSerializer(SerializerWrapper):
    class Meta:
        model = Payment
        exclude = (
            'invoice',
            )

    def run_validation(self, data):
        validated = super(PaymentSerializer, self).run_validation(data)
        if 'id' in validated:
            return self.Meta.model.objects.get(id=validated['id'])
        return self.Meta.model(**dict(validated))

class InvoiceSerializer(SerializerWrapper):
    date = serializers.DateField(format="%Y-%m-%d")
    provider_name = serializers.ReadOnlyField(source='provider.name')
    paid = CheckboxField()
    payment_set = PaymentSerializer(many=True, required=False)

    class Meta:
        model = Invoice
        fields = '__all__'

    # def validate_payment_set(self, value):
    #     return self.validate_reverse_field(value, Payment, "payment_set")

    def create(self, validated_data):
        instance = super(InvoiceSerializer, self).create(validated_data)
        instance.recalculate_payments()
        return instance

    def update(self, instance, validated_data):
        instance = super(InvoiceSerializer, self).update(instance, validated_data)
        instance.recalculate_payments()
        return instance

class CollectionSerializer(SerializerWrapper):
    class Meta:
        model = Collection
        fields = '__all__'

class SellSerializer(SerializerWrapper):
    customer_name = serializers.ReadOnlyField(source='customer.name')
    paid = CheckboxField()
    collection_set = CollectionSerializer(many=True)

    class Meta:
        model = Sell
        fields = '__all__'

    def validate_collection_set(self, value):
        return self.validate_reverse_field(value, Collection, "collection_set")

    def create(self, validated_data):
        instance = super(SellSerializer, self).create(validated_data)
        instance.recalculate_collections()
        return instance

    def update(self, instance, validated_data):
        instance = super(SellSerializer, self).update(instance, validated_data)
        instance.recalculate_collections()
        return instance

class CollectionSerializer(SerializerWrapper):
    class Meta:
        model = Collection
        fields = '__all__'

class WorkSerializer(SerializerWrapper):
    class Meta:
        model = Work
        fields = '__all__'

class EmployeeWorkSerializer(SerializerWrapper):
    class Meta:
        model = Employee_Work
        fields = '__all__'