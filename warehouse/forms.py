from django import forms
from django.utils.encoding import (
    force_str, force_text, python_2_unicode_compatible,
)
from django.utils.html import conditional_escape, format_html
from django.forms.utils import flatatt
from django.utils.safestring import mark_safe

from warehouse.models import Product, Brand, Provider, Appliance, Organization, Input, Output, Lending, Order

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

class HiddenField(forms.Field):
    widget = forms.widgets.HiddenInput

    def __init__(self, *args, **kwargs):
        super(HiddenField, self).__init__(label='', *args, **kwargs)


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

class NewInputForm(forms.ModelForm):
    action = HiddenField(initial='new')

    class Meta:
        model = Input
        fields = '__all__'


class EditInputForm(forms.ModelForm):
    id = HiddenField()
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
