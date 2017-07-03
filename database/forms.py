from django import forms
from django.utils import timezone

from database.models import *
from database.serializers import PercentageSerializer
from datetime import datetime, date, timedelta

from mysite.forms import *

import json

class NewProductForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label="Marca", widget=Datalist())
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor", widget=Datalist())
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    appliance = forms.ModelChoiceField(queryset=Appliance.objects.all(), required=False, label="Aplicacion", widget=Datalist())
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=False, initial=0, min_value=0, max_value=100)
    action = HiddenField(initial='new')

    class Meta:
        model = Product
        fields = [
            "code",
            "brand",
            "provider",
            "name",
            "description",
            "appliance",
            "price",
            "discount",
            ]

class EditProductForm(forms.ModelForm):
    code = forms.CharField(max_length=30, label='Codigo')
    brand = forms.ModelChoiceField(queryset=Brand.objects.all(), required=False, label="Marca", widget=Datalist())
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor", widget=Datalist())
    name = forms.CharField(max_length=200, label='Nombre')
    description = forms.CharField(max_length=255, label='Descripcion', required=False)
    appliance = forms.ModelChoiceField(queryset=Appliance.objects.all(), required=False, label="Aplicacion", widget=Datalist())
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio de lista', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=False, initial=0, min_value=0, max_value=100)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Product
        fields = [
            "code",
            "brand",
            "provider",
            "name",
            "description",
            "appliance",
            "price",
            "discount",
            ]

class DeleteProductForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Product
        fields = ["id"]

class ProviderContactForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    department = forms.CharField(max_length=200, label='Departamento')
    email = forms.EmailField(max_length=255, label='Email', required=False)
    phone = forms.CharField(max_length=200, label='Telefono')
    for_orders = forms.BooleanField(label="Para pedidos")

    class Meta:
        model = Provider_Contact
        fields = '__all__'


class NewProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    contacts = forms.ModelChoiceField(queryset=Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ProviderContactForm()), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Provider
        fields = '__all__'


class EditProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    contacts = forms.ModelChoiceField(queryset=Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ProviderContactForm()), empty_label=None)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Provider
        fields = '__all__'


class DeleteProviderForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Provider
        fields = ["id"]

class ContactForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    department = forms.CharField(max_length=200, label='Departamento')
    email = forms.EmailField(max_length=255, label='Email', required=False)
    phone = forms.CharField(max_length=200, label='Telefono')

    class Meta:
        model = Contact
        fields = '__all__'

class NewCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    contacts = forms.ModelChoiceField(queryset=Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ContactForm()), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Customer
        fields = '__all__'


class EditCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    contacts = forms.ModelChoiceField(queryset=Contact.objects.none(), required=True, label="Contactos", widget=FormSet(form=ContactForm()), empty_label=None)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Customer
        fields = '__all__'


class DeleteCustomerForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Customer
        fields = ["id"]

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


class DeleteEmployeeForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Employee
        fields = ["id"]

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


class DeleteBrandForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Brand
        fields = ["id"]

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


class DeleteApplianceForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Appliance
        fields = ["id"]

class NewPercentageForm(forms.ModelForm):
    max_price_limit = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio maximo', required=True, min_value=0, initial=0)
    percentage_1 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 1', required=True, min_value=0, initial=0)
    percentage_2 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 2', required=True, min_value=0, initial=0)
    percentage_3 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 3', required=True, min_value=0, initial=0)
    action = HiddenField(initial='new')

    class Meta:
        model = Percentage
        fields = '__all__'


class EditPercentageForm(forms.ModelForm):
    max_price_limit = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio maximo', required=True, min_value=0, initial=0)
    percentage_1 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 1', required=True, min_value=0, initial=0)
    percentage_2 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 2', required=True, min_value=0, initial=0)
    percentage_3 = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento 3', required=True, min_value=0, initial=0)
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Percentage
        fields = '__all__'


class DeletePercentageForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Percentage
        fields = ["id"]

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


class DeleteOrganizationForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Organization
        fields = ["id"]

class NewOrganizationStorageForm(forms.ModelForm):
    action = HiddenField(initial='new')

    class Meta:
        model = Organization_Storage
        fields = '__all__'


class EditOrganizationStorageForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Organization_Storage
        fields = '__all__'


class DeleteOrganizationStorageForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Organization_Storage
        fields = ["id"]

class NewInputForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M:%S"))
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.order_by('number'), label="Factura", widget=Datalist())
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Input
        fields = ('date', 'organization_storage', 'invoice', 'products')

class EditInputForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateTimeInput(), label='Fecha')
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.order_by('number'), label="Factura")
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Input
        fields = ('date', 'organization_storage', 'invoice', 'products')


class DeleteInputForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Input
        fields = ["id"]

class NewOutputForm(forms.ModelForm):
    date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M:%S"))
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True, include=["in_storage"]), empty_label=None)
    employee = forms.ModelChoiceField(queryset=Employee.objects.order_by('name'), label="Empleado")
    destination = forms.ModelChoiceField(queryset=Customer.objects.order_by('name'), label="Destino")
    replacer = forms.ModelChoiceField(queryset=Organization.objects.order_by('name'), label="Repone")
    action = HiddenField(initial='new')

    class Meta:
        model = Output
        fields = '__all__'


class EditOutputForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateTimeInput(), label='Fecha')
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True, include=["in_storage"]), empty_label=None)
    employee = forms.ModelChoiceField(queryset=Employee.objects.order_by('name'), label="Empleado")
    destination = forms.ModelChoiceField(queryset=Customer.objects.order_by('name'), label="Destino")
    replacer = forms.ModelChoiceField(queryset=Organization.objects.order_by('name'), label="Repone")
    action = HiddenField(initial='edit')

    class Meta:
        model = Output
        fields = '__all__'


class DeleteOutputForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Output
        fields = ["id"]

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


class DeleteLendingForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Lending
        fields = ["id"]

class NewOrderForm(forms.ModelForm):
    action = HiddenField(initial='new')
    # date = forms.DateTimeField(widget=DateTimeInput(), label='Fecha', initial=timezone.localtime(timezone.now()).strftime("%Y-%m-%dT%H:%M:%S"))
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    provider = forms.ModelChoiceField(queryset=Provider.objects.all(), required=False, label="Proveedor")
    claimant = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, label="Solicitante")
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen", empty_label=None)

    class Meta:
        model = Order
        fields = (
            # 'date',
            'message',
            'provider',
            'organization_storage',
            'claimant',
            'products',
        )


class EditOrderForm(forms.ModelForm):
    id = HiddenField()
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    claimant = forms.ModelChoiceField(queryset=Employee.objects.all(), required=False, label="Solicitante")
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen", empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Order
        fields = (
            'provider',
            'organization_storage',
            'claimant',
            'products',
        )


class DeleteOrderForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Order
        fields = ["id"]

class NewInvoiceForm(forms.ModelForm):
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    credit = forms.DecimalField(max_digits=9, decimal_places=2, label='Credito', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=True, min_value=0, initial=0)
    paid = forms.BooleanField(label="Pagado?")
    action = HiddenField(initial='new')

    class Meta:
        model = Invoice
        fields = '__all__'


class EditInvoiceForm(forms.ModelForm):
    id = HiddenField()
    number = forms.CharField(max_length=200, label='Numero')
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    due = forms.DateField(widget=DateInput(), label='Vence')
    price = forms.DecimalField(max_digits=9, decimal_places=2, label='Precio total', required=True, min_value=0, initial=0)
    credit = forms.DecimalField(max_digits=9, decimal_places=2, label='Credito', required=True, min_value=0, initial=0)
    discount = forms.DecimalField(max_digits=9, decimal_places=2, label='Descuento', required=True, min_value=0, initial=0)
    paid = forms.BooleanField(label="Pagado?")
    action = HiddenField(initial='edit')

    class Meta:
        model = Invoice
        fields = '__all__'


class DeleteInvoiceForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Invoice
        fields = ["id"]

class NewQuotationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Quotation
        fields = '__all__'


class EditQuotationForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Quotation
        fields = '__all__'


class DeleteQuotationForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Quotation
        fields = ["id"]

class NewPriceListForm(forms.ModelForm):
    customer = forms.ModelChoiceField(queryset=Customer.objects.all(), required=False, label="Cliente")#, widget=Datalist())
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    percentages = HiddenField(initial=json.dumps(PercentageSerializer(Percentage.objects.all(), many=True).data))
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(editable_fields=["price"]), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = PriceList
        fields = '__all__'


class EditPriceListForm(forms.ModelForm):
    id = HiddenField()
    base_price = forms.ChoiceField(required=False, label="Precio Base", choices = ([('', 'Precio base'), ('sale_percentage_1','Precio de Venta 1'), ('sale_percentage_2','Precio de Venta 2'),('sale_percentage_3','Precio de Venta 3'), ('service_percentage_1','Precio de Servicio 1'), ('service_percentage_2','Precio de Servicio 2'),('service_percentage_3','Precio de Servicio 3')]))
    percentages = HiddenField(initial=json.dumps(PercentageSerializer(Percentage.objects.all(), many=True).data))
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(editable_fields=["price"]), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = PriceList
        fields = '__all__'


class DeletePriceListForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = PriceList
        fields = ["id"]

class NewPaymentForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Payment
        fields = '__all__'


class EditPaymentForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Payment
        fields = '__all__'


class DeletePaymentForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Payment
        fields = ["id"]

class NewWorkForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Work
        fields = '__all__'


class EditWorkForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Work
        fields = '__all__'


class DeleteWorkForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Work
        fields = ["id"]

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

class OrderOutputForm(forms.ModelForm):
    id = HiddenField()
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    claimant = forms.CharField(max_length=200, label='Solicitante')
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='order')

    class Meta:
        model = Output
        fields = ['message', 'organization_storage', 'claimant', 'products']


class InputOrderForm(forms.ModelForm):
    id = HiddenField()
    invoice = forms.ModelChoiceField(queryset=Invoice.objects.order_by('number'), label="Numero de factura", widget=Datalist())
    invoice_date = forms.DateField(widget=DateInput(), label='Fecha de Factura', initial=datetime.now())
    organization_storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    products = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='input')

    class Meta:
        model = Input
        fields = ('invoice_date', 'invoice', 'organization_storage', 'products')


class MailOrderForm(forms.ModelForm):
    id = HiddenField()
    message = forms.CharField(widget=forms.Textarea(attrs={"class":"form-control"}), label="Mensaje", initial="Por medio de este mensaje les solicitamos el siguiente pedido. Favor de confirmar por esta misma via si esta enderado del mismo.\nDuda o aclaracion comunicarlo con almacenista a cargo.\nGracias.")
    action = HiddenField(initial='mail')

    class Meta:
        model = Output
        fields = ['message']


class DateRangeFilterForm(forms.Form):
    date__gte = forms.DateField(widget=DateInput(), initial=date.today() - timedelta(28), label='Desde')
    date__lt = forms.DateField(widget=DateInput(), initial=date.today() + timedelta(1), label='Hasta')

class DateTimeRangeFilterForm(forms.Form):
    date__gte = forms.DateTimeField(widget=DateTimeInput(), initial=datetime(year=(datetime.now() - timedelta(28)).year, month=(datetime.now() - timedelta(28)).month, day=(datetime.now() - timedelta(28)).day).strftime(format="%Y-%m-%dT%H:%M:%S"), label='Desde')
    date__lt = forms.DateTimeField(widget=DateTimeInput(), initial=datetime(year=datetime.now().year, month=datetime.now().month, day=datetime.now().day, hour=23, minute=59).strftime(format="%Y-%m-%dT%H:%M:%S"), label='Hasta')
