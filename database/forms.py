from django import forms
from django.utils import timezone

from database.models import *
from database.serializers import PercentageSerializer
from datetime import datetime, date, timedelta

from mysite.forms import *

import json

cached_objects = {
    "product":{
        "model": Product,
        "name_fields": ["code", "name", "description"]
    },
    "provider":{
        "model": Provider
    },
    "employee":{
        "model": Employee,
    },
    "customer": {
        "model": Customer,
    },
    "pricelist": {
        "model": PriceList,
        "name_fields": ["customer_name"]
    },
    "organization":{
        "model": Organization,
    },
    "organization_storage":{
        "model": Organization_Storage,
        "name_fields": ["organization_name", "storage_type_name"]
    },
    "movement_product":{
        "model": Movement_Product,
        "related_model": "product"
    },
    "order_product":{
        "model": Order_Product,
        "related_model": "product",
    },
    "quotation_product": {
        "model": Quotation_Product,
        "related_model": "product",
    },
    "pricelist_product": {
        "model": PriceList_Product,
        "related_model": "product",
    },
    "employee_work": {
        "model": Employee_Work,
        "related_model": "employee"
    }
}

class CachedModelChoiceField(forms.ModelChoiceField):

    def __init__(self, name, *args, **kwargs):
        super().__init__(queryset=cached_objects[name]["model"].objects.none(), *args, **kwargs)
        self.widget.attrs["class"] = "{} cached-model".format(self.widget.attrs.get("class", ""))
        self.widget.attrs["data-namers"] = json.dumps(cached_objects[name].get("name_fields"))
        self.widget.attrs["data-name"] = name
        self.widget.attrs["widget"] = self.widget.__class__.__name__

class CachedRelatedModelChoiceField(CachedModelChoiceField):

    def __init__(self, name, *args, **kwargs):
        super().__init__(name, *args, **kwargs)
        self.widget.attrs["data-name"] = cached_objects[name]["related_model"]
        self.widget.attrs["data-namers"] = json.dumps(cached_objects[cached_objects[name]["related_model"]].get("name_fields"))


class DeleteForm(forms.Form):
    id = HiddenField()
    action = HiddenField(initial='delete')

class NewProductForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    brand_name = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label="Marca", widget=Datalist())
    provider_name = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor", widget=Datalist())
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    appliance_name = forms.ModelChoiceField(queryset=Appliance.objects.all(), required=False, label="Aplicacion", widget=Datalist())
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=False, initial=0, min_value=0, max_value=100)
    picture = forms.ImageField(label="Foto")
    action = HiddenField(initial='new')

    class Meta:
        model = Product
        fields = [
            "code",
            "brand_name",
            "provider_name",
            "name",
            "description",
            "appliance_name",
            "price",
            "discount",
            "picture",
            ]

class EditProductForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    brand_name = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label="Marca", widget=Datalist())
    provider_name = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor", widget=Datalist())
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    appliance_name = forms.ModelChoiceField(queryset=Appliance.objects.all(), required=False, label="Aplicacion", widget=Datalist())
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=False, initial=0, min_value=0, max_value=100)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Product
        fields = [
            "code",
            "brand_name",
            "provider_name",
            "name",
            "description",
            "appliance_name",
            "price",
            "discount",
            ]

class ProviderContactForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    department = forms.CharField(max_length=200, label='Departamento')
    email = forms.EmailField(max_length=255, label='Email', required=False)
    phone = forms.CharField(max_length=200, label='Telefono')
    for_orders = forms.BooleanField(label="Para pedidos")

    class Meta:
        model = Provider_Contact
        fields = ('name', 'department', 'email', 'phone', 'for_orders')


class NewProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    provider_contact_set = forms.ModelChoiceField(queryset=Provider_Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ProviderContactForm()), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Provider
        fields = '__all__'


class EditProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    provider_contact_set = forms.ModelChoiceField(queryset=Provider_Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ProviderContactForm()), empty_label=None)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Provider
        fields = '__all__'

class CustomerContactForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    department = forms.CharField(max_length=200, label='Departamento')
    email = forms.EmailField(max_length=255, label='Email', required=False)
    phone = forms.CharField(max_length=200, label='Telefono')
    for_quotation = forms.BooleanField(label="Para cotizaciones")
    for_invoice = forms.BooleanField(label="Para factura")

    class Meta:
        model = Customer_Contact
        fields = ('name', 'department', 'email', 'phone', 'for_quotation', 'for_invoice')

class NewCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    customer_contact_set = forms.ModelChoiceField(queryset=Customer_Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=CustomerContactForm()), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Customer
        fields = ("name",)


class EditCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    customer_contact_set = forms.ModelChoiceField(queryset=Customer_Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=CustomerContactForm()), empty_label=None)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Customer
        fields = ("name",)

class MergeCustomerForm(forms.ModelForm):
    name = forms.ModelChoiceField(queryset=Customer.objects.all(), empty_label=None, required=True, label='Nombre Correcto')
    ids = HiddenField()
    action = HiddenField(initial='merge')

    class Meta:
        model = Customer
        fields = ("name",)

class NewEmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Employee
        fields = '__all__'


class EditEmployeeForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Employee
        fields = '__all__'

class NewBrandForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Brand
        fields = '__all__'


class EditBrandForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Brand
        fields = '__all__'

class NewApplianceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Appliance
        fields = '__all__'


class EditApplianceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Appliance
        fields = '__all__'

class NewPercentageForm(forms.ModelForm):
    max_price_limit = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio maximo', required=True, min_value=0, initial=0)
    # percentage_1 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 1', required=True, min_value=0, initial=0)
    # percentage_2 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 2', required=True, min_value=0, initial=0)
    # percentage_3 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 3', required=True, min_value=0, initial=0)
    action = HiddenField(initial='new')

    class Meta:
        model = Percentage
        fields = '__all__'


class EditPercentageForm(forms.ModelForm):
    max_price_limit = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio maximo', required=True, min_value=0, initial=0)
    # percentage_1 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 1', required=True, min_value=0, initial=0)
    # percentage_2 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 2', required=True, min_value=0, initial=0)
    # percentage_3 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 3', required=True, min_value=0, initial=0)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Percentage
        fields = '__all__'

class NewOrganizationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Organization
        fields = '__all__'


class EditOrganizationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Organization
        fields = '__all__'

class NewOrganizationStorageForm(forms.ModelForm):
    action = HiddenField(initial='new')
    storage_type_name = forms.ModelChoiceField(queryset=StorageType.objects.all(), required=False, label="Tipo", widget=Datalist())

    class Meta:
        model = Organization_Storage
        fields = [
            'organization'
        ]


class EditOrganizationStorageForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')
    storage_type_name = forms.ModelChoiceField(queryset=StorageType.objects.all(), required=False, label="Tipo", widget=Datalist())

    class Meta:
        model = Organization_Storage
        fields = [
            'organization'
        ]

class NewInputForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    provider = CachedModelChoiceField(name="provider", required=True, label="Proveedor")
    invoice_number = forms.CharField(max_length=200, label='Numero de factura')
    invoice_date = forms.DateField(widget=DateInput(), label='Fecha de Factura', initial=datetime.now())
    evidence = forms.ImageField(label="Evidencia")
    movement_product_set = CachedRelatedModelChoiceField(name="movement_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price'], extra_fields={'discount':{'tag':'input', 'type': 'number'}}), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Input
        fields = [
            'date',
            'evidence',
            'organization_storage',
            'provider'
        ]

class EditInputForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateTimeInput(), label='Fecha')
    evidence = forms.ImageField(label="Evidencia")
    action = HiddenField(initial='edit')

    class Meta:
        model = Input
        fields = [
            'date'
        ]

class NewOutputForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    movement_product_set = CachedRelatedModelChoiceField(name="movement_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price']), empty_label=None)
    employee = CachedModelChoiceField(name="employee", label="Empleado")
    destination = CachedModelChoiceField(name="customer", label="Destino")
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    evidence = forms.ImageField(label="Evidencia")
    action = HiddenField(initial='new')

    class Meta:
        model = Output
        fields = '__all__'


class EditOutputForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateTimeInput(), label='Fecha')
    employee = CachedModelChoiceField(name="employee", label="Empleado")
    destination = CachedModelChoiceField(name="customer", label="Destino")
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    evidence = forms.ImageField(label="Evidencia")
    action = HiddenField(initial='edit')

    class Meta:
        model = Output
        fields = [
            'date',
            'employee',
            'destination',
            'replacer',
            'evidence'
        ]

class NewLendingForm(forms.ModelForm):
    action = HiddenField(initial='new')

    class Meta:
        model = Lending
        fields = '__all__'


class EditLendingForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Lending
        fields = '__all__'

class NewOrderForm(forms.ModelForm):
    action = HiddenField(initial='new')
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    email_override = forms.EmailField(max_length=255, label='Email alternativo', required=False)
    order_product_set = CachedRelatedModelChoiceField(name="order_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True), empty_label=None)
    provider = CachedModelChoiceField(name="provider", required=False, label="Proveedor")
    claimant = CachedModelChoiceField(name="employee", required=False, label="Solicitante")
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen", empty_label=None)

    class Meta:
        model = Order
        fields = (
            'message',
            'email_override',
            'provider',
            'organization_storage',
            'claimant',
            'replacer',
            'order_product_set',
        )


class EditOrderForm(forms.ModelForm):
    id = HiddenField()
    claimant = CachedModelChoiceField(name="employee", required=False, label="Solicitante")
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen", empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Order
        fields = (
            'organization_storage',
            'claimant',
            'replacer',
        )

class QuotationOtherForm(forms.ModelForm):
    description = forms.CharField(max_length=200, label='Descripcion')
    amount = forms.IntegerField(label='Cantidad', required=True, min_value=0, initial=0)
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio unitario', required=True, min_value=0, initial=0)

    class Meta:
        model = Quotation_Others
        fields = (
            'description',
            'amount',
            'price'
        )

class NewQuotationForm(forms.ModelForm):
    action = HiddenField(initial='new')
    unit = forms.CharField(max_length=60, label='Unidad')
    plates = forms.CharField(max_length=10, label='Placas')
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('pricelist', 'Lista de precios'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    # percentages = HiddenJSONField(PercentageSerializer)
    pricelist = CachedModelChoiceField(name="pricelist", required=False, label="Lista de precios")
    customer = CachedModelChoiceField(name="customer", required=False, label="Cliente")
    quotation_product_set = CachedRelatedModelChoiceField(name="quotation_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price']), empty_label=None)
    quotation_others_set = forms.ModelChoiceField(queryset=Quotation_Others.objects.none(), required=True, label="Otros", widget=FormSet(form=QuotationOtherForm()), empty_label=None)
    service = forms.DecimalField(max_digits=9, decimal_places=2, label='Costo del servicio', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento en pesos', required=True, min_value=0, initial=0)
    iva = forms.BooleanField(label="+IVA")
    work_number = forms.IntegerField(required=False, label="Numero de hoja")
    authorized = forms.BooleanField(label="Autorizado")
    unit_section = forms.ChoiceField(choices=Quotation.SECTION_CHOICES, widget=ColumnCheckboxWidget(), label="Secciones")

    class Meta:
        model = Quotation
        fields = (
            'unit',
            'plates',
            'base_price',
            'pricelist',
            'customer',
            'quotation_product_set',
            'quotation_others_set',
            'service',
            'discount',
            'iva',
            'work_number',
            'authorized',
        )


class EditQuotationForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')
    unit = forms.CharField(max_length=60, label='Unidad')
    plates = forms.CharField(max_length=10, label='Placas')
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('pricelist', 'Lista de precios'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    pricelist = HiddenField()
    customer = HiddenField()
    quotation_product_set = CachedRelatedModelChoiceField(name="quotation_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price']), empty_label=None)
    quotation_others_set = forms.ModelChoiceField(queryset=Quotation_Others.objects.none(), required=True, label="Otros", widget=FormSet(form=QuotationOtherForm()), empty_label=None)
    service = forms.DecimalField(max_digits=9, decimal_places=2, label='Costo del servicio', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento en pesos', required=True, min_value=0, initial=0)
    iva = forms.BooleanField(label="+IVA")
    work_number = forms.IntegerField(required=False, label="Numero de hoja")
    authorized = forms.BooleanField(label="Autorizado")
    unit_section = forms.ChoiceField(choices=Quotation.SECTION_CHOICES, widget=ColumnCheckboxWidget(), label="Secciones")

    class Meta:
        model = Quotation
        fields = (
            'id',
            'unit',
            'plates',
            'base_price',
            'pricelist',
            'customer',
            'quotation_product_set',
            'quotation_others_set',
            'service',
            'discount',
            'iva',
            'work_number',
            'authorized'
        )

class NewPriceListForm(forms.ModelForm):
    customer = CachedModelChoiceField(name="customer", required=False, label="Cliente")#, widget=Datalist())
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    percentages = HiddenJSONField(PercentageSerializer)
    pricelist_product_set = CachedRelatedModelChoiceField(name="pricelist_product", required=False, label="Refacciones", widget=MultiSetWidget(editable_fields=['price']), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = PriceList
        fields = '__all__'


class EditPriceListForm(forms.ModelForm):
    id = HiddenField()
    customer = HiddenField()
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    percentages = HiddenJSONField(PercentageSerializer)
    pricelist_product_set = CachedRelatedModelChoiceField(name="pricelist_product", required=False, label="Refacciones", widget=MultiSetWidget(editable_fields=['price']), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = PriceList
        fields = '__all__'

class PaymentForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    amount = forms.DecimalField(max_digits=9, decimal_places=2, label='Cantidad', required=True, min_value=0, initial=0)
    method = forms.ChoiceField(choices=Collection.METHOD_CHOICES, label="Forma de pago")

    class Meta:
        model = Payment
        fields = ('date', 'amount', 'method')

class NewInvoiceForm(forms.ModelForm):
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    invoiced = forms.BooleanField(required=False, label="Facturado")
    action = HiddenField(initial='new')

    class Meta:
        model = Invoice
        fields = (
            "number",
            "date",
            "due",
            "provider",
            "price",
            "invoiced",
        )


class EditInvoiceForm(forms.ModelForm):
    id = HiddenField()
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    payment_set = forms.ModelChoiceField(queryset=Payment.objects.none(), required=True, label="Pagos", widget=FormSet(form=PaymentForm()), empty_label=None)
    invoiced = forms.BooleanField(required=False, label="Facturado")
    action = HiddenField(initial='edit')

    class Meta:
        model = Invoice
        fields = (
            "number",
            "date",
            "due",
            "provider",
            "price",
            "invoiced",
        )

class CollectionForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    amount = forms.DecimalField(max_digits=9, decimal_places=2, label='Cantidad', required=True, min_value=0, initial=0)
    method = forms.ChoiceField(choices=Collection.METHOD_CHOICES, label="Forma de pago")

    class Meta:
        model = Payment
        fields = ('date', 'amount', 'method')

class NewSellForm(forms.ModelForm):
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, label="Cliente")
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    action = HiddenField(initial='new')

    class Meta:
        model = Sell
        fields = (
            "number",
            "date",
            "due",
            "customer",
            "price"
        )


class EditSellForm(forms.ModelForm):
    id = HiddenField()
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, label="Cliente")
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    invoiced = forms.BooleanField(required=False, label="Facturado")
    collection_set = forms.ModelChoiceField(queryset=Collection.objects.none(), required=True, label="Cobros", widget=FormSet(form=CollectionForm()), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Sell
        fields = (
            "number",
            "date",
            "due",
            "customer",
            "price",
            "invoiced"
        )

class NewCollectionForm(forms.ModelForm):
    action = HiddenField(initial='new')

    class Meta:
        model = Collection
        fields = '__all__'


class EditCollectionForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Collection
        fields = '__all__'

class NewWorkForm(forms.ModelForm):
    number = forms.IntegerField(label="Numero")
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    employee_work_set = CachedRelatedModelChoiceField(name="employee_work", required=False, label="Trabajadores", widget=MultiSetWidget(), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Work
        fields = (
            'number',
            'date'
        )


class EditWorkForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    employee_work_set = CachedRelatedModelChoiceField(name="employee_work", required=False, label="Trabajadores", widget=MultiSetWidget(), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Work
        fields = (
            'date',
        )

class ChangeStorageProductForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')
    product = HiddenField()
    organization_storage = HiddenField()
    amount = forms.IntegerField(label='Cantidad')
    must_have = forms.IntegerField(label="Debe haber")

    class Meta:
        model = Storage_Product
        fields = ["id", "action", "amount", "must_have"]

class QuotationMailForm(forms.Form):
    id = HiddenField()
    subject = forms.CharField(label="Asunto", initial="Cotizacion de Muelles Obrero")
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="Por medio de este mensaje se envia la siguente cotizacion")
    action = HiddenField(initial='mail')

class QuotationSellForm(forms.ModelForm):
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    customer = HiddenField()
    price = HiddenField()
    action = HiddenField(initial='sell')

    class Meta:
        model = Sell
        fields = (
            "number",
            "date",
            "due",
            "customer",
            "price"
        )

class QuotationOutputForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=datetime.now().strftime("%Y-%m-%dT%H:%M:%S"))
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    movement_product_set = CachedRelatedModelChoiceField(name="movement_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price']), empty_label=None)
    employee = CachedModelChoiceField(name="employee", label="Empleado")
    destination = HiddenField()
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    action = HiddenField(initial='output')

    class Meta:
        model = Output
        fields = (
            'date',
            'organization_storage',
            'employee',
            'replacer',
            'movement_product_set',
            'destination'
        )

class OrderOutputForm(forms.ModelForm):
    id = HiddenField()
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    email_override = forms.EmailField(max_length=255, label='Email alternativo', required=False)
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    claimant = CachedModelChoiceField(name="employee", label="Solicitante")
    replacer = CachedModelChoiceField(name="organization", label="Repone")
    order_product_set = CachedRelatedModelChoiceField(name="movement_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True), empty_label=None)
    action = HiddenField(initial='order')

    class Meta:
        model = Output
        fields = ['message', 'email_override', 'organization_storage', 'claimant']

class EmailOutputForm(forms.Form):
    email = forms.EmailField(max_length=255, label='Email', required=False)
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="")
    ids = HiddenField()
    action = HiddenField(initial='email')

class InputOrderForm(forms.ModelForm):
    order_id = HiddenField()
    invoice = HiddenField()
    provider = HiddenField()
    invoice_number = forms.CharField(max_length=200, label='Numero de factura')
    invoice_date = forms.DateField(widget=DateInput(), label='Fecha de Factura', initial=datetime.now())
    evidence = forms.ImageField(label="Evidencia")
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    movement_product_set = CachedRelatedModelChoiceField(name="movement_product", required=False, label="Refacciones", widget=MultiSetWidget(amounts=True, editable_fields=['price'], extra_fields={'discount':{'tag':'input', 'type': 'number'}}), empty_label=None)
    action = HiddenField(initial='input')

    class Meta:
        model = Input
        fields = ('invoice', 'invoice_date', 'invoice_number', 'evidence', 'organization_storage', 'movement_product_set')


class MailOrderForm(forms.ModelForm):
    id = HiddenField()
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    email_override = forms.EmailField(max_length=255, label='Email alternativo', required=False)
    organization_storage = HiddenField()
    action = HiddenField(initial='mail')

    class Meta:
        model = Output
        fields = ['organization_storage']

class AddStorageProductForm(forms.ModelForm):
    organization_storage = CachedModelChoiceField(name="organization_storage", required=True, label="Almacen")
    product = CachedModelChoiceField(name="product", required=True, label="Product")
    amount = forms.IntegerField(label='Cantidad')
    must_have = forms.IntegerField(label="Debe haber")
    action = HiddenField(initial='new')

    class Meta:
        model = Storage_Product
        fields = '__all__'


class DateRangeFilterForm(forms.Form):
    date__gte = forms.DateField(widget=DateInput(), initial=date.today() - timedelta(28), label='Desde')
    date__lt = forms.DateField(widget=DateInput(), initial=date.today() + timedelta(1), label='Hasta')

class DateTimeRangeFilterForm(forms.Form):
    date__gte = forms.DateTimeField(widget=DateTimeInput(), initial=datetime(year=(datetime.now() - timedelta(28)).year, month=(datetime.now() - timedelta(28)).month, day=(datetime.now() - timedelta(28)).day).strftime(format="%Y-%m-%dT%H:%M:%S"), label='Desde')
    date__lt = forms.DateTimeField(widget=DateTimeInput(), initial=datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=23, minute=59).strftime(format="%Y-%m-%dT%H:%M:%S"), label='Hasta')

class InvoiceProviderFilterForm(forms.Form):
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), label="Proveedor")

class UploadPictureForm(forms.ModelForm):
    id = HiddenField()
    picture = forms.ImageField(label="Foto")
    action = HiddenField(initial='picture')

    class Meta:
        model = Product
        fields = ['picture']

class RemovePhotoForm(forms.Form):
    ids = HiddenField()
    action = HiddenField(initial='remove_photo')