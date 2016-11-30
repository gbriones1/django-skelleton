from __future__ import unicode_literals

from django.db import models

VALID_FIELDS = ['Field', 'CharField']

def get_fields(cls):
    fields = []
    for field in cls._meta.fields:
        if field.__class__.__base__.__name__ in VALID_FIELDS and field.__class__.__name__ != 'AutoField':
            fields.append((field.name, field.formfield().label, field.__class__.__name__))
        elif field.__class__.__name__ == 'ForeignKey':
            fields.append((field.name, field.target_field.model.__name__, field.__class__.__name__))
    return fields

models.Model.get_fields = classmethod(get_fields)

class Appliance(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def products_related(self):
        products = Product.objects.filter(appliance=self)
        return len(products)

class Provider(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(blank=True, null=True)

    def __unicode__(self):
        return self.name

    def products_related(self):
        products = Product.objects.filter(provider=self)
        return len(products)

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def products_related(self):
        products = Product.objects.filter(brand=self)
        return len(products)

class Tool(models.Model):
    code = models.CharField(max_length=30, unique=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, null=True, blank=True)
    condition = models.CharField(max_length=255, null=True, blank=True)

    def __unicode__(self):
        return self.code+" - "+self.name+" - "+self.description

class Product(models.Model):
    code = models.CharField(max_length=30, unique=True)
    brand = models.ForeignKey(Brand, null=True, blank=True)
    provider = models.ForeignKey(Provider, null=True, blank=True)
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=255, null=True, blank=True)
    appliance = models.ForeignKey(Appliance, null=True, blank=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.code+" - "+self.name.encode('utf8')+" - "+self.description

    def __unicode__(self):
        return self.code+" - "+self.name+" - "+self.description

class Organization(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class StorageType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

class Organization_Storage(models.Model):
    organization = models.ForeignKey(Organization)
    storage_type = models.ForeignKey(StorageType)
    products = models.ManyToManyField(Product, through="Storage_Product")
    tools = models.ManyToManyField(Tool, through="Storage_Tool")

class Storage_Product(models.Model):
    product = models.ForeignKey(Product)
    organization_storage = models.ForeignKey(Organization_Storage)
    amount = models.IntegerField()

class Storage_Tool(models.Model):
    tool = models.ForeignKey(Tool)
    organization_storage = models.ForeignKey(Organization_Storage)
    amount = models.IntegerField()

class Percentage(models.Model):
    max_price_limit = models.DecimalField(max_digits=9, decimal_places=2)
    percentage_1 = models.DecimalField(max_digits=9, decimal_places=2)
    percentage_2 = models.DecimalField(max_digits=9, decimal_places=2)
    percentage_3 = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return self.max_price_limit

class Movement(models.Model):
    date = models.DateTimeField()
    organization_storage = models.ForeignKey(Organization_Storage)

class Input(models.Model):
    movement = models.ForeignKey(Movement)
    invoice_number = models.CharField(max_length=30, null=True, blank=True)

class Output(models.Model):
    movement = models.ForeignKey(Movement)
    employee = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    replacer = models.ForeignKey(Organization, null=True, blank=True)

class Lending(models.Model):
    movement = models.ForeignKey(Movement)
    employee = models.CharField(max_length=100)
    destination = models.CharField(max_length=100)
    returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True)

class Input_Product(models.Model):
    input_reg = models.ForeignKey(Input)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Output_Product(models.Model):
    output_reg = models.ForeignKey(Output)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Lending_Product(models.Model):
    lending = models.ForeignKey(Lending)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

class Lending_Tool(models.Model):
    lending = models.ForeignKey(Lending)
    tool = models.ForeignKey(Tool)
    amount = models.IntegerField()
    returned_amount = models.IntegerField()

class Order(models.Model):
    STATUS_PENDING = 'P'
    STATUS_ASKED = 'A'
    STATUS_CANCELED = 'C'
    STATUS_RECEIVED = 'R'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Por pedir'),
        (STATUS_ASKED, 'Pedido'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_RECEIVED, 'Recibido'),
    )
    date = models.DateTimeField(auto_now_add=True)
    provider = models.ForeignKey(Provider)
    claimant = models.CharField(max_length=100, null=True, blank=True)

class Order_Product(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    organization_storage = models.ForeignKey(Organization_Storage)
    status = models.CharField(max_length=1, choices=Order.STATUS_CHOICES, null=True)
    received_date = models.DateTimeField(null=True)

class Configuration(models.Model):
    sender_email = models.EmailField(null=True)
    password = models.CharField(max_length=30, null=True)
    receiver_email = models.EmailField(null=True)
    mailOnPriceChange = models.BooleanField(default=True)
    mailOnNegativeValues = models.BooleanField(default=True)
    # destination del sistema para enviar un correo de adgoritmo para mi hermoso amorcito te amo te amo :*
    # la longitud de mi inteligencia va a ayudar a mi papito clo voy a ayudar siempre
