from __future__ import unicode_literals

import json
import os

from datetime import datetime

from PIL import Image

from django.db import models
from django.utils import timezone

class Appliance(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def products_related(self):
        products = Product.objects.filter(appliance=self)
        return len(products)

    class Meta:
        ordering = ['name']

class Brand(models.Model):
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    def products_related(self):
        products = Product.objects.filter(brand=self)
        return len(products)

    class Meta:
        ordering = ['name']

class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def products_related(self):
        products = Product.objects.filter(provider=self)
        return len(products)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Provider_Contact(models.Model):
    provider = models.ForeignKey(Provider)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    for_orders = models.BooleanField(default=False)

class Invoice(models.Model):
    number = models.CharField(max_length=30)
    date = models.DateField()
    due = models.DateField(null=True)
    provider = models.ForeignKey(Provider, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    credit = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'date')

    def recalculate_payments(self, *args, **kwargs):
        acc = 0
        for payment in self.payment_set.all():
            acc += float(payment.amount)
        if round(acc, 2) >= float(self.price):
            self.paid = True
        else:
            self.paid = False
        self.save()

    def recalculate_price(self):
        price = 0.0
        for input_reg in self.input_set.all():
            for mp in input_reg.movement_product_set.all():
                price += float(mp.price) * mp.amount
        self.price = price
        self.save()

class Payment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    invoice = models.ForeignKey(Invoice)

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Customer_Contact(models.Model):
    customer = models.ForeignKey(Customer)
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    for_quotation = models.BooleanField(default=False)
    for_invoice = models.BooleanField(default=False)

class Sell(models.Model):
    number = models.CharField(max_length=30)
    date = models.DateField()
    due = models.DateField(null=True)
    customer = models.ForeignKey(Customer, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    credit = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    discount = models.DecimalField(max_digits=9, decimal_places=2, null=True)
    paid = models.BooleanField(default=False)

    def __unicode__(self):
        return self.number

    class Meta:
        unique_together = ('number', 'date')

    def recalculate_collections(self, *args, **kwargs):
        acc = 0
        for collection in self.collection_set.all():
            acc += float(collection.amount)
        if round(acc, 2) >= float(self.price):
            self.paid = True
        else:
            self.paid = False
        self.save()

class Collection(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    sell = models.ForeignKey(Sell)

class Employee(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15, null=True)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

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
    picture = models.ImageField(upload_to='products/', null=True)

    @property
    def real_price(self):
        return "${:.2f}".format(self.get_real_price())

    @property
    def in_storage(self):
        storage_products = Storage_Product.objects.filter(product=self)
        result = {}
        for sp in storage_products:
            result[sp.organization_storage.id] = sp.amount
        return json.dumps(result)

    @property
    def percentage_1(self):
        percentage = Percentage.objects.filter(max_price_limit__gte=self.price)
        sell_price = self.get_real_price()
        if percentage:
            sell_price = sell_price+sell_price*percentage[0].sale_percentage_1/100
        return "${:.2f}".format(sell_price)

    @property
    def percentage_2(self):
        percentage = Percentage.objects.filter(max_price_limit__gte=self.price)
        sell_price = self.get_real_price()
        if percentage:
            sell_price = sell_price+sell_price*percentage[0].sale_percentage_2/100
        return "${:.2f}".format(sell_price)

    @property
    def percentage_3(self):
        percentage = Percentage.objects.filter(max_price_limit__gte=self.price)
        sell_price = self.get_real_price()
        if percentage:
            sell_price = sell_price+sell_price*percentage[0].sale_percentage_3/100
        return "${:.2f}".format(sell_price)

    @property
    def pricelist_related(self):
        return [int(x.pricelist.id) for x in PriceList_Product.objects.filter(product=self)]

    def get_real_price(self):
        return self.price-(self.price*(self.discount/100))

    def __str__(self):
        if self.appliance:
            return self.code+" - "+self.name.encode('ascii', 'ignore')+" - "+self.description.encode('ascii', 'ignore')+" - "+self.appliance.name
        return self.code+" - "+self.name.encode('ascii', 'ignore')+" - "+self.description.encode('ascii', 'ignore')

    def __unicode__(self):
        return self.code+" - "+self.name+" - "+self.description

    class Meta:
        ordering = ['code']

    def save(self, *args, **kwargs):
        obj_copy = self
        if self.id:
            obj_copy = Product.objects.get(id=self.id)
        if self.picture:
            if obj_copy.picture and obj_copy.picture != self.picture:
                os.remove(obj_copy.picture.file.name)
            super(Product, self).save(*args, **kwargs)
            picture = Image.open(self.picture.file)
            picture.thumbnail((500,500), Image.ANTIALIAS)
            picture.save(self.picture.file.name)
        else:
            if obj_copy.picture:
                os.remove(obj_copy.picture.file.name)
            super(Product, self).save(*args, **kwargs)


    def delete(self, *args, **kwargs):
        if self.picture:
            os.remove(self.picture.file.name)
        super(Product, self).delete(*args, **kwargs)


class Organization(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class StorageType(models.Model):
    name = models.CharField(max_length=200)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Organization_Storage(models.Model):
    organization = models.ForeignKey(Organization)
    storage_type = models.ForeignKey(StorageType)

    def __unicode__(self):
        return self.organization.name + " - " + self.storage_type.name

    class Meta:
        ordering = ['organization']

class Storage_Product(models.Model):
    organization_storage = models.ForeignKey(Organization_Storage)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    must_have = models.IntegerField(null=True)

    @property
    def product_code(self):
        return self.product.code

    @property
    def product_name(self):
        return self.product.name

    @property
    def product_description(self):
        return self.product.description

    @property
    def product_brand(self):
        return self.product.brand.name

    @property
    def storage_name(self):
        return self.organization_storage.storage_type.name

    @property
    def organization_name(self):
        return self.organization_storage.organization.name

class Storage_Tool(models.Model):
    organization_storage = models.ForeignKey(Organization_Storage)
    tool = models.ForeignKey(Tool)
    amount = models.IntegerField()

class Percentage(models.Model):
    max_price_limit = models.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_1 = models.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_2 = models.DecimalField(max_digits=9, decimal_places=2)
    sale_percentage_3 = models.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_1 = models.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_2 = models.DecimalField(max_digits=9, decimal_places=2)
    service_percentage_3 = models.DecimalField(max_digits=9, decimal_places=2)

    def __unicode__(self):
        return str(self.max_price_limit)

class PriceList(models.Model):
    customer = models.OneToOneField(Customer)

    def __unicode__(self):
        return self.customer.name

class PriceList_Product(models.Model):
    pricelist = models.ForeignKey(PriceList)
    product = models.ForeignKey(Product)
    alt_code = models.CharField(max_length=30, null=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def __str__(self):
        return self.product.code+" - "+self.product.name.encode('ascii', 'ignore')+" - "+self.product.description.encode('ascii', 'ignore')

    def __unicode__(self):
        return self.product.code+" - "+self.product.name+" - "+self.product.description

class Quotation(models.Model):
    date = models.DateTimeField(default=datetime.now)
    pricelist = models.ForeignKey(PriceList, null=True)
    customer = models.ForeignKey(Customer, null=True)
    unit = models.CharField(max_length=30, null=True)
    plates = models.CharField(max_length=30, null=True)
    authorized = models.BooleanField(default=False)
    service = models.DecimalField(max_digits=9, decimal_places=2)
    discount = models.DecimalField(max_digits=9, decimal_places=2)
    work_sheet = models.IntegerField(null=True)

    def customer_name(self):
        return self.customer.name

class Quotation_Product(models.Model):
    quotation = models.ForeignKey(Quotation)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Quotation_Others(models.Model):
    quotation = models.ForeignKey(Quotation)
    description = models.CharField(max_length=60)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Work(models.Model):
    date = models.DateField()
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)
    unit_section = models.CharField(max_length=30, null=True)
    quotation = models.ForeignKey(Quotation, null=True)

class Employee_Work(models.Model):
    work = models.ForeignKey(Work)
    employee = models.ForeignKey(Employee)
    earning = models.DecimalField(max_digits=9, decimal_places=2)

    class Meta:
        unique_together = ('work', 'employee',)

class Movement(models.Model):
    date = models.DateTimeField(default=datetime.now)
    organization_storage = models.ForeignKey(Organization_Storage)

    def delete(self, *args, **kwargs):
        for mp in self.movement_product_set.all():
            mp.delete()
        if self.get_type() == "Input" and self.invoice:
            self.invoice.recalculate_price()
        return super(Movement, self).delete(*args, **kwargs)

    def get_type(self):
        try:
            self.input
            return "Input"
        except:
            return "Output"

class Movement_Product(models.Model):
    movement = models.ForeignKey(Movement, null=True)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

    def save(self, *args, **kwargs):
        sp = Storage_Product.objects.filter(organization_storage=self.movement.organization_storage, product=self.product)
        if sp:
            sp = sp[0]
        else:
            sp = Storage_Product(organization_storage=self.movement.organization_storage, product=self.product, amount=0, must_have=0)
        difference = self.amount
        if self.id:
            old = Movement_Product.objects.get(id=self.id)
            difference -= old.amount
        if self.movement.get_type() != "Input":
            difference *= -1
        sp.amount += difference
        sp.save()
        return super(Movement_Product, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        sp = Storage_Product.objects.filter(organization_storage=self.movement.organization_storage, product=self.product)
        if sp:
            sp = sp[0]
        else:
            sp = Storage_Product(organization_storage=self.movement.organization_storage, product=self.product, amount=0, must_have=0)
        difference = self.amount
        if self.movement.get_type() == "Input":
            difference *= -1
        sp.amount += difference
        sp.save()
        return super(Movement_Product, self).delete(*args, **kwargs)

class Input(Movement):
    invoice = models.ForeignKey(Invoice, null=True)

class Output(Movement):
    employee = models.ForeignKey(Employee, null=True)
    destination = models.ForeignKey(Customer, null=True)
    replacer = models.ForeignKey(Organization, null=True, blank=True)

class Lending(models.Model):
    date = models.DateTimeField(default=datetime.now)
    organization_storage = models.ForeignKey(Organization_Storage)
    employee = models.ForeignKey(Employee, null=True)
    customer = models.ForeignKey(Customer, null=True)
    returned = models.BooleanField(default=False)
    returned_date = models.DateTimeField(null=True)
    products = models.ManyToManyField(Product, through='Lending_Product')

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
    STATUS_INCOMPLETE = 'I'
    STATUS_CHOICES = (
        (STATUS_PENDING, 'Por pedir'),
        (STATUS_ASKED, 'Pedido'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_RECEIVED, 'Recibido'),
        (STATUS_INCOMPLETE, 'Incompleto'),
    )
    date = models.DateTimeField(default=datetime.now)
    provider = models.ForeignKey(Provider)
    organization_storage = models.ForeignKey(Organization_Storage)
    claimant = models.ForeignKey(Employee, null=True)
    replacer = models.ForeignKey(Organization, null=True, blank=True)
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, null=True, default=STATUS_PENDING)
    received_date = models.DateTimeField(null=True)

    @property
    def order_product(self):
        return Order_Product.objects.filter(order=self)

    @order_product.setter
    def order_product(self, products):
        self.products_desc = products

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        if hasattr(self, 'products_desc'):
            for op in self.products_desc:
                product = Product.objects.get(id=op['product'])
                if op['status'] == 'new':
                    order_product = Order_Product(order=self, product=product, amount=int(op["amount"]))
                    order_product.save()
                elif op['status'] == 'update':
                    order_product = self.order_product.get(id=op['id'])
                    order_product.amount = int(op['amount'])
                    order_product.save()
                elif op['status'] == 'delete':
                    order_product = self.order_product.get(id=op['id'])
                    order_product.delete()

    def delete(self, *args, **kwargs):
        for op in self.order_product:
            op.delete()
        super(Order, self).delete(*args, **kwargs)

class Order_Product(models.Model):
    order = models.ForeignKey(Order)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    amount_received = models.IntegerField(default=0)

class Configuration(models.Model):
    sender_email = models.EmailField(null=True)
    password = models.CharField(max_length=30, null=True)
    quotations_email = models.EmailField(null=True)
    quotations_password = models.CharField(max_length=30, null=True)
    receiver_email = models.EmailField(null=True)
    mailOnPriceChange = models.BooleanField(default=True)
    mailOnNegativeValues = models.BooleanField(default=True)
    # destination del sistema para enviar un correo de adgoritmo para mi hermoso amorcito te amo te amo :*
    # la longitud de mi inteligencia va a ayudar a mi papito clo voy a ayudar siempre
