from django import forms
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.utils.html import conditional_escape, format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe
from django.core import serializers

from database.models import (
    Provider, Customer, Employee, Brand, Appliance, Product, Percentage, Organization,
    StorageType, Organization_Storage, Storage_Product, PriceList,
    Input, Output, Lending, Order, Quotation, Invoice, Payment, Work,
)
from datetime import datetime
import json

class Datalist(forms.widgets.Select):
    def render(self, name, value, attrs=None, choices=()):
        if value is None:
            value = ''
        datalist_attrs = attrs
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs["list"] = final_attrs.pop("id")
        if value != '':
            if name == "brand":
                final_attrs["value"] = Brand.objects.get(id=value).name
            elif name == "provider":
                final_attrs["value"] = Provider.objects.get(id=value).name
        output = [format_html('<input{} />', flatatt(final_attrs)), format_html('<datalist{}>', flatatt(datalist_attrs))]
        options = self.render_options(choices, [value])
        if options:
            output.append(options)
        output.append('</datalist>')
        return mark_safe('\n'.join(output))

    def render_option(self, selected_choices, option_value, option_label):
        if option_value is None:
            option_value = ''
        if option_value == "":
            option_label = ""
        option_value = force_text(option_value)
        return format_html('<option value="{}"></option>',
                           force_text(option_label))

class MultiSet(forms.widgets.Select):

    def __init__(self, search=True, amounts=False):
        super(forms.widgets.Select, self).__init__()
        self.search = search
        self.amounts = amounts

    def render(self, name, value, attrs=None, choices=()):
        model_name = self.choices.queryset.model.__name__
        if value is None:
            value = ''
        final_attrs = self.build_attrs(attrs, name=name)
        final_attrs["type"] = 'hidden'
        output = []
        output.append(format_html('<div{}>', flatatt({"class": "row"})))
        output.append(format_html('<div{}>', flatatt({"class": "col-sm-6", "style":"height: 600px;overflow-y: auto;padding: 0"})))
        output.append(format_html('<table{} >', flatatt({"class": "table", "id":model_name+"MultiSet-table"})))
        for choice in self.choices.queryset:
            tr_attr = json.loads(serializers.serialize("json", [choice]))[0]['fields']
            tr_attr = dict([("data-"+x, tr_attr[x].encode("ascii", "ignore")) if type(tr_attr[x]) == type(u"") else ("data-"+x, tr_attr[x]) for x in tr_attr.keys()])
            tr_attr["data-id"] = choice.id
            output.append(format_html('<tr {}>', flatatt(tr_attr)))
            output.append('<td>{}</td>'.format(str(choice)))
            output.append(format_html('<td><button{}>+</button></td>', flatatt({"class":"btn btn-primary btn-sm "+model_name+"MultiSet-add", "type":"button"})))
            output.append('</tr>')
        output.append('</table>')
        output.append('</div>')

        output.append(format_html('<div{}>', flatatt({"class": "col-sm-6", "style":"height: 600px;overflow-y: auto;padding: 0"})))
        output.append(format_html('<table{} >', flatatt({"class": "table", 'id':model_name+"MultiSet-added"})))
        output.append('</table>')
        output.append('</div>')
        output.append('</div>')

        if self.search or self.amounts:
            output.append(format_html('<div{}>', flatatt({"class": "row"})))
            output.append(format_html('<div{}>', flatatt({"class": "col-sm-6"})))
            output.append(format_html('<table{} >', flatatt({})))
            output.append('<tr>')
            if self.search:
                output.append(format_html('<td><input{} /></td>', flatatt({"placeholder":"Search", "id":model_name+"MultiSet-search"})))
            if self.amounts:
                output.append(format_html('<td> X </td>', flatatt({})))
                output.append(format_html('<td><input{} /></td>', flatatt({"value":"1", "type":"number", "min":"1", "id":model_name+"MultiSet-multiplier"})))
            output.append('</tr>')
            output.append('</table>')
            output.append('</div>')
            output.append('</div>')

        output.append(format_html('<input{} />', flatatt(final_attrs)))
        output.append('<script>var modelName="'+model_name+'"; var inputSetId="'+final_attrs["id"]+'"</script>')

        return mark_safe('\n'.join(output))


class HiddenField(forms.Field):
    widget = forms.widgets.HiddenInput

    def __init__(self, *args, **kwargs):
        super(HiddenField, self).__init__(label='', *args, **kwargs)

class DateInput(forms.DateInput):
    input_type = 'date'


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


class NewProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    email = forms.EmailField(max_length=255, label='Email', required=False)
    action = HiddenField(initial='new')

    class Meta:
        model = Provider
        fields = '__all__'


class EditProviderForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    email = forms.EmailField(max_length=255, label='Email', required=False)
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

class NewCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Customer
        fields = '__all__'


class EditCustomerForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
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
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    input_product_set = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='new')

    class Meta:
        model = Input
        fields = '__all__'
        exclude = ('movement',)


class EditInputForm(forms.ModelForm):
    id = HiddenField()
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    input_product_set = forms.ModelChoiceField(queryset=Product.objects.all(), required=True, label="Refacciones", widget=MultiSet(amounts=True), empty_label=None)
    action = HiddenField(initial='edit')

    class Meta:
        model = Input
        fields = '__all__'


class DeleteInputForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Input
        fields = ["id"]

class NewOutputForm(forms.ModelForm):
    date = forms.DateField(widget=DateInput(), label='Fecha', initial=datetime.now())
    storage = forms.ModelChoiceField(queryset=Organization_Storage.objects.all(), required=True, label="Almacen")
    action = HiddenField(initial='new')

    class Meta:
        model = Output
        fields = '__all__'


class EditOutputForm(forms.ModelForm):
    id = HiddenField()
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

    class Meta:
        model = Order
        fields = '__all__'


class EditOrderForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='edit')

    class Meta:
        model = Order
        fields = '__all__'


class DeleteOrderForm(forms.ModelForm):
    id = HiddenField()
    action = HiddenField(initial='delete')

    class Meta:
        model = Order
        fields = ["id"]

class NewInvoiceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    action = HiddenField(initial='new')

    class Meta:
        model = Invoice
        fields = '__all__'


class EditInvoiceForm(forms.ModelForm):
    name = forms.CharField(max_length=200, label='Nombre')
    id = HiddenField()
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
