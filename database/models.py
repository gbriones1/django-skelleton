from __future__ import unicode_literals

import json
import os

from datetime import datetime

from PIL import Image

from django.db import models
from django.utils import timezone

VALID_FIELDS = ['Field', 'CharField', 'DateTimeCheckMixin', 'DateField', 'FileField']

def get_fields(cls, remove_fields=[], add_fields=[]):
    fields = []
    for field in cls._meta.fields:
        if field.name not in remove_fields:
            if field.__class__.__base__.__name__ in VALID_FIELDS and field.__class__.__name__ != 'AutoField':
                fields.append((field.name, field.formfield().label, field.__class__.__name__))
            elif field.__class__.__name__ == 'ForeignKey':
                fields.append((field.name, field.target_field.model.__name__, field.__class__.__name__))
    return fields+add_fields

models.Model.get_fields = classmethod(get_fields)

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

class Contact(models.Model):
    name = models.CharField(max_length=100)
    department = models.CharField(max_length=100, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    phone = models.CharField(max_length=15, blank=True, null=True)

    def __unicode__(self):
        return self.name + " - " + self.department

class Provider(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contacts = models.ManyToManyField(Contact, through='Provider_Contact')

    @property
    def provider_contact(self):
        return Provider_Contact.objects.filter(provider=self)

    @provider_contact.setter
    def provider_contact(self, contacts):
        self.contacts_desc = contacts

    def __unicode__(self):
        return self.name

    def save(self, *args, **kwargs):
        super(Provider, self).save(*args, **kwargs)
        if hasattr(self, 'contacts_desc'):
            for c in self.contacts_desc:
                if c['status'] == 'new':
                    contact = Contact(name=c['name'], department=c['department'], email=c['email'], phone=c['phone'])
                    contact.save()
                    provider_contact = Provider_Contact(provider=self, contact=contact, for_orders=bool(c["for_orders"]))
                    provider_contact.save()
                elif c['status'] == 'update':
                    provider_contact = self.provider_contact.get(id=c['id'])
                    provider_contact.contact.name = c['name']
                    provider_contact.contact.department = c['department']
                    provider_contact.contact.email = c['email']
                    provider_contact.contact.phone = c['phone']
                    provider_contact.contact.save()
                    provider_contact.for_orders = c['for_orders']
                    provider_contact.save()
                elif c['status'] == 'delete':
                    provider_contact = self.provider_contact.get(id=c['id'])
                    contact = provider_contact.contact
                    provider_contact.delete()
                    contact.delete()

    def delete(self, *args, **kwargs):
        for pc in self.provider_contact:
            contact = pc.contact
            pc.delete()
            contact.delete()
        super(Provider, self).delete(*args, **kwargs)

    def products_related(self):
        products = Product.objects.filter(provider=self)
        return len(products)

    class Meta:
        ordering = ['name']

class Provider_Contact(models.Model):
    provider = models.ForeignKey(Provider)
    contact = models.ForeignKey(Contact)
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

    def save(self, *args, **kwargs):
        super(Invoice, self).save(*args, **kwargs)
        acc = 0
        for payment in self.payment_set.all():
            acc += float(payment.amount)
        if round(acc, 2) >= float(self.price):
            self.paid = True
        else:
            self.paid = False
        super(Invoice, self).save(*args, **kwargs)

    def recalculate_price(self):
        price = 0.0
        for input_reg in self.input_set.all():
            for mp in input_reg.movement_product:
                price += float(mp.price) * mp.amount
        self.price = price
        self.save()

class Payment(models.Model):
    date = models.DateField()
    amount = models.DecimalField(max_digits=9, decimal_places=2)
    invoice = models.ForeignKey(Invoice)

class Customer(models.Model):
    name = models.CharField(max_length=100, unique=True)
    contacts = models.ManyToManyField(Contact)

    def __unicode__(self):
        return self.name

    @property
    def customer_contact(self):
        return Contact.objects.filter(customer=self)

    @customer_contact.setter
    def customer_contact(self, contacts):
        self.contacts_desc = contacts

    def save(self, *args, **kwargs):
        if hasattr(self, 'contacts_desc'):
            for c in self.contacts_desc:
                if c['status'] == 'new':
                    contact = Contact(name=c['name'], department=c['department'], email=c['email'], phone=c['phone'])
                    contact.save()
                    self.contacts.add(contact)
                elif c['status'] == 'update':
                    contact = self.contacts.get(id=c['id'])
                    contact.name = c['name']
                    contact.department = c['department']
                    contact.email = c['email']
                    contact.phone = c['phone']
                    contact.save()
                elif c['status'] == 'delete':
                    contact = self.contacts.get(id=c['id'])
                    contact.delete()
        super(Customer, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        for cc in self.contacts:
            cc.delete()
        super(Customer, self).delete(*args, **kwargs)

    class Meta:
        ordering = ['name']

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

    def save(self, *args, **kwargs):
        super(Sell, self).save(*args, **kwargs)
        acc = 0
        for collection in self.collection_set.all():
            acc += float(collection.amount)
        if round(acc, 2) >= float(self.price):
            self.paid = True
        else:
            self.paid = False
        super(Sell, self).save(*args, **kwargs)

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
        if self.picture:
            obj_copy = Product.objects.get(id=self.id)
            if obj_copy.picture and obj_copy.picture != self.picture:
                os.remove(obj_copy.picture.file.name)
            super(Product, self).save(*args, **kwargs)
            picture = Image.open(self.picture.file)
            picture.thumbnail((500,500), Image.ANTIALIAS)
            picture.save(self.picture.file.name)
        else:
            obj_copy = Product.objects.get(id=self.id)
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

    @property
    def pricelist_product(self):
        return PriceList_Product.objects.filter(pricelist=self)

    @pricelist_product.setter
    def pricelist_product(self, products):
        self.products_desc = products

    def save(self, *args, **kwargs):
        super(PriceList, self).save(*args, **kwargs)
        if hasattr(self, 'products_desc'):
            for pp in self.products_desc:
                product = Product.objects.get(id=pp['product'])
                if pp['status'] == 'new':
                    pricelist_product = PriceList_Product(pricelist=self, product=product, price=float(pp["price"]))
                    pricelist_product.save()
                elif pp['status'] == 'update':
                    pricelist_product = self.pricelist_product.get(id=pp['id'])
                    pricelist_product.price = float(pp['price'])
                    pricelist_product.save()
                elif pp['status'] == 'delete':
                    pricelist_product = self.pricelist_product.get(id=pp['id'])
                    pricelist_product.delete()

    def delete(self, *args, **kwargs):
        for pp in self.pricelist_product:
            pp.delete()
        super(PriceList, self).delete(*args, **kwargs)

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

    @property
    def quotation_product(self):
        return Quotation_Product.objects.filter(quotation=self)

    @quotation_product.setter
    def quotation_product(self, products):
        self.products_desc = products

    @property
    def quotation_other(self):
        return Quotation_Others.objects.filter(quotation=self)

    @quotation_other.setter
    def quotation_other(self, others):
        self.others_desc = others

    def save(self, *args, **kwargs):
        super(Quotation, self).save(*args, **kwargs)
        if hasattr(self, 'products_desc'):
            for qp in self.products_desc:
                product = Product.objects.get(id=qp['product'])
                if qp['status'] == 'new':
                    quotation_product = Quotation_Product(quotation=self, product=product, amount=int(qp["amount"]), price=float(qp["price"]))
                    quotation_product.save()
                elif qp['status'] == 'update':
                    quotation_product = self.quotation_product.get(id=qp['id'])
                    quotation_product.price = float(qp['price'])
                    quotation_product.amount = int(qp['amount'])
                    quotation_product.save()
                elif qp['status'] == 'delete':
                    quotation_product = self.quotation_product.get(id=qp['id'])
                    quotation_product.delete()
        if hasattr(self, 'others_desc'):
            for qo in self.others_desc:
                if qo['status'] == 'new':
                    quotation_other = Quotation_Others(quotation=self, description=qo["description"], amount=int(qo["amount"]), price=float(qo["price"]))
                    quotation_other.save()
                elif qo['status'] == 'update':
                    quotation_other = self.quotation_other.get(id=qo['id'])
                    quotation_other.description = qo['description']
                    quotation_other.price = float(qo['price'])
                    quotation_other.amount = int(qo['amount'])
                    quotation_other.save()
                elif qo['status'] == 'delete':
                    quotation_other = self.quotation_other.get(id=qo['id'])
                    quotation_other.delete()

    def delete(self, *args, **kwargs):
        for qp in self.quotation_product:
            qp.delete()
        for qo in self.quotation_other:
            qo.delete()
        super(Quotation, self).delete(*args, **kwargs)

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
    products = models.ManyToManyField(Product, through='Movement_Product')

    def save(self, *args, **kwargs):
        super(Movement, self).save(*args, **kwargs)
        if hasattr(self, 'products_desc'):
            for mp in self.products_desc:
                product = Product.objects.get(id=mp['product'])
                if mp['status'] == 'new':
                    movement_product = Movement_Product(movement=self, product=product, amount=int(mp["amount"]), price=float(mp['price']))
                    movement_product.save()
                elif mp['status'] == 'update':
                    movement_product = self.movement_product.get(id=mp['id'])
                    movement_product.amount = int(mp['amount'])
                    movement_product.price = float(mp['price'])
                    movement_product.save()
                elif mp['status'] == 'delete':
                    movement_product = self.movement_product.get(id=mp['id'])
                    movement_product.delete()
                for organization_storage_id in mp['restock'].keys():
                    organization_storage = Organization_Storage.objects.get(id=organization_storage_id)
                    storage_product = Storage_Product.objects.get(organization_storage=organization_storage, product=product)
                    storage_product.amount += mp['restock'][organization_storage_id]
                    storage_product.save()

    def delete(self, *args, **kwargs):
        for mp in self.movement_product:
            storage_product = Storage_Product.objects.get(organization_storage=self.organization_storage, product=mp.product)
            diff = mp.amount
            if self.__class__.__name__ == "Input":
                diff *= -1
            storage_product.amount += diff
            storage_product.save()
            mp.delete()
        super(Movement, self).delete(*args, **kwargs)

class Movement_Product(models.Model):
    movement = models.ForeignKey(Movement, null=True)
    product = models.ForeignKey(Product)
    amount = models.IntegerField()
    price = models.DecimalField(max_digits=9, decimal_places=2)

class Input(Movement):
    invoice = models.ForeignKey(Invoice, null=True)

    @property
    def movement_product(self):
        return Movement_Product.objects.filter(movement=self)

    @movement_product.setter
    def movement_product(self, products):
        self.products_desc = products


class Output(Movement):
    employee = models.ForeignKey(Employee, null=True)
    destination = models.ForeignKey(Customer, null=True)
    replacer = models.ForeignKey(Organization, null=True, blank=True)

    @property
    def movement_product(self):
        return Movement_Product.objects.filter(movement=self)

    @movement_product.setter
    def movement_product(self, products):
        self.products_desc = products

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
    receiver_email = models.EmailField(null=True)
    mailOnPriceChange = models.BooleanField(default=True)
    mailOnNegativeValues = models.BooleanField(default=True)
    # destination del sistema para enviar un correo de adgoritmo para mi hermoso amorcito te amo te amo :*
    # la longitud de mi inteligencia va a ayudar a mi papito clo voy a ayudar siempre
