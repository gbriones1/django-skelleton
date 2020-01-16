from django.test import TestCase
from django.test.client import RequestFactory

from database.serializers import *
from database.models import *

rf = RequestFactory()

class ProductTestCase(TestCase):
    PRODUCTS_DATA = [
        {
            "code": "0000",
            "name": "TEST",
            "providerName": "TEST",
            "brandName": "TEST",
            "applianceName": "",
            "price": 50.50,
            "discount": 0.0,
        },
        {
            "code": "0001",
            "name": "TEST2",
            "providerName": "TEST2",
            "brandName": "TEST",
            "applianceName": "TEST2",
            "price": 100,
            "discount": 30
        }
    ]

    def test_product_create(self):
        data = ProductTestCase.PRODUCTS_DATA[0]
        s = ProductSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i = s.instance
        self.assertGreaterEqual(i.id, 1)
        self.assertGreaterEqual(i.brand.id, 1)
        self.assertGreaterEqual(i.provider.id, 1)
        data = ProductTestCase.PRODUCTS_DATA[1]
        s = ProductSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i2 = s.instance
        self.assertEqual(i2.brand.id, i.brand.id)
        self.assertNotEqual(i2.provider.id, i.provider.id)


    def test_product_create_dup(self):
        data = ProductTestCase.PRODUCTS_DATA[0]
        s = ProductSerializer(data=data)
        s.is_valid()
        s.save()
        s = ProductSerializer(data=data)
        self.assertFalse(s.is_valid())

class InputTestCase(TestCase):

    def setUp(self):
        s = ProductSerializer(data=ProductTestCase.PRODUCTS_DATA, many=True)
        s.is_valid()
        s.save()
        self.products = s.instance
        s = OrganizationSerializer(data={"name":"Storage1"})
        s.is_valid()
        s.save()
        self.organization = s.instance
        s = OrganizationStorageSerializer(data={
            "organization":self.organization.id,
            "storage_type":"Stock"
            })
        s.is_valid()
        s.save()
        self.organization_storage = s.instance

    def test_input_create(self):
        data = {
            "organization_storage": self.organization_storage.id,
            "invoice": "00000",
            "invoice_date": "2019-02-27",
            "movement_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 5,
                "price": 50.55,
                "discount": 50
            }])
        }
        s = InputSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i = s.instance
        self.assertGreaterEqual(i.id, 1)
        p = i.movement_product_set.get(product=self.products[0].id).product
        self.assertEqual(float(p.discount), 50)
        self.assertEqual(float(p.price), 50.55)
        data2 = {
            "organization_storage": self.organization_storage.id,
            "invoice": "00001",
            "invoice_date": "2019-02-28",
            "movement_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 4,
                "price": 60,
                "discount": 30
            }])
        }
        s = InputSerializer(data=data2)
        self.assertTrue(s.is_valid())
        s.save()
        i2 = s.instance
        self.assertGreaterEqual(i2.id, 2)
        p = i2.movement_product_set.get(product=self.products[0]).product
        self.assertEqual(float(p.discount), 30)
        self.assertEqual(float(p.price), 60)
        sp = Storage_Product.objects.get(organization_storage=self.organization_storage, product=self.products[0])
        self.assertEqual(sp.amount, 9)
        self.assertEqual(i2.invoice.price, 168)
        data3 = {
            "organization_storage": self.organization_storage.id,
            "invoice": "00000",
            "invoice_date": "2019-02-27",
            "movement_product_set": json.dumps([{
                "product": self.products[1].id,
                "amount": 10,
                "price": 120,
                "discount": 20
            }])
        }
        s = InputSerializer(data=data3)
        self.assertTrue(s.is_valid())
        s.save()
        i3 = s.instance
        self.assertEqual(i3.invoice.id, i.invoice.id)
        self.assertEqual(float(i3.invoice.price), 1086.38)



class OutputTestCase(TestCase):

    def setUp(self):
        s = ProductSerializer(data=ProductTestCase.PRODUCTS_DATA, many=True)
        s.is_valid()
        s.save()
        self.products = s.instance
        s = OrganizationSerializer(data={"name":"Storage1"})
        s.is_valid()
        s.save()
        self.organization = s.instance
        s = OrganizationStorageSerializer(data={
            "organization":self.organization.id,
            "storage_type_name":"Stock"
            })
        s.is_valid()
        s.save()
        self.organization_storage = s.instance

    def test_output_create(self):
        data = {
            "organization_storage": self.organization_storage.id,
            "movement_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 7,
                "price": 50.55,
            }])
        }
        s = OutputSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i = s.instance
        sp = Storage_Product.objects.get(organization_storage=self.organization_storage, product=self.products[0])
        self.assertEqual(sp.amount, 2)
        data = {
            "employee": self.employees[0].id,
            "destination": self.customers[0].id,
            "replacer": self.organizations[0].id,
            "organization_storage": self.organization_storage.id,
            "movement_product_set": [json.dumps([{
                "product": self.products[0].id,
                "amount": 1,
                "price": 50.55,
            }])]
        }
        s = OutputSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i = s.instance
        sp = Storage_Product.objects.get(organization_storage=self.organization_storage, product=self.products[0])
        self.assertEqual(sp.amount, 1)
        self.assertEqual(i.employee.id, self.employees[0].id)
        self.assertEqual(i.destination.id, self.customers[0].id)
        self.assertEqual(i.replacer.id, self.organizations[0].id)

    def test_output_exeed(self):
        data = {
            "organization_storage": self.organization_storage.id,
            "movement_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 50000,
                "price": 50.55,
            }])
        }
        s = OutputSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        i = s.instance
        sp = Storage_Product.objects.get(organization_storage=self.organization_storage, product=self.products[0])
        self.assertEqual(sp.amount, 0)

    def test_unexistent(self):
        data = {
            "organization_storage": 90000,
            "movement_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 7,
                "price": 50.55,
            }])
        }
        s = OutputSerializer(data=data)
        self.assertFalse(s.is_valid())
        data = {
            "organization_storage": self.organization_storage.id,
            "movement_product_set": json.dumps([{
                "product": 90000,
                "amount": 7,
                "price": 50.55,
            }])
        }
        s = OutputSerializer(data=data)
        self.assertFalse(s.is_valid())

class EmployeeTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "Employee"
        }
        s = EmployeeSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Employee")
        self.employees = [s.instance]
    
    def test_edit(self):
        data = {
            "id": self.employees[0].id,
            "name": "new name"
        }
        s = EmployeeSerializer(self.employees[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "new name")
        self.assertEqual(s.instance.phone, self.employees[0].phone)
        self.assertEqual(s.instance.id, self.employees[0].id)
        data["phone"] = "1234567890"
        s = EmployeeSerializer(self.employees[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.phone, "1234567890")
        self.assertEqual(s.instance.id, self.employees[0].id)

class CustomerTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "Customer"
        }
        s = CustomerSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Customer")
        self.customers = [s.instance]

    def test_edit(self):
        data = {
            "id": self.customers[0].id,
            "name": "new name"
        }
        s = CustomerSerializer(self.customers[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "new name")
        self.assertEqual(s.instance.id, self.customers[0].id)
        self.assertEqual(len(s.instance.customer_contact_set.all()), 0)
        data["customer_contact_set"] = json.dumps([{
            "name": "contact1"
        },{
            "name": "contact2",
            "email": "contact@customer.com",
            "for_quotation": True,
            "for_invoice": False,
        }])
        s = CustomerSerializer(self.customers[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.id, self.customers[0].id)
        self.assertEqual(len(s.instance.customer_contact_set.all()), 2)
        self.assertEqual(s.instance.customer_contact_set.all()[0].name, "contact1")
        self.assertEqual(s.instance.customer_contact_set.all()[0].email, "")
        self.assertEqual(s.instance.customer_contact_set.all()[0].for_quotation, False)
        self.assertEqual(s.instance.customer_contact_set.all()[1].name, "contact2")
        self.assertEqual(s.instance.customer_contact_set.all()[1].email, "contact@customer.com")
        self.assertEqual(s.instance.customer_contact_set.all()[1].for_quotation, True)

class ProviderTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "Provider"
        }
        s = ProviderSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Provider")
        self.providers = [s.instance]

    def test_edit(self):
        data = {
            "id": self.providers[0].id,
            "name": "new name"
        }
        s = ProviderSerializer(self.providers[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "new name")
        self.assertEqual(s.instance.id, self.providers[0].id)
        self.assertEqual(len(s.instance.provider_contact_set.all()), 0)
        data["provider_contact_set"] = json.dumps([{
            "name": "contact1"
        },{
            "name": "contact2",
            "email": "contact@provider.com",
            "for_orders": True
        }])
        s = ProviderSerializer(self.providers[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.id, self.providers[0].id)
        self.assertEqual(len(s.instance.provider_contact_set.all()), 2)
        self.assertEqual(s.instance.provider_contact_set.all()[0].name, "contact1")
        self.assertEqual(s.instance.provider_contact_set.all()[0].email, "")
        self.assertEqual(s.instance.provider_contact_set.all()[0].for_orders, False)
        self.assertEqual(s.instance.provider_contact_set.all()[1].name, "contact2")
        self.assertEqual(s.instance.provider_contact_set.all()[1].email, "contact@provider.com")
        self.assertEqual(s.instance.provider_contact_set.all()[1].for_orders, True)
        data["provider_contact_set"] = json.dumps([{
            "name": "contact3"
        },{
            "name": "contact2",
            "email": "contact2@provider.com"
        }])
        s = ProviderSerializer(self.providers[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.id, self.providers[0].id)
        self.assertEqual(len(s.instance.provider_contact_set.all()), 2)
        self.assertEqual(s.instance.provider_contact_set.all()[0].name, "contact3")
        self.assertEqual(s.instance.provider_contact_set.all()[0].email, "")
        self.assertEqual(s.instance.provider_contact_set.all()[0].for_orders, False)
        self.assertEqual(s.instance.provider_contact_set.all()[1].name, "contact2")
        self.assertEqual(s.instance.provider_contact_set.all()[1].email, "contact2@provider.com")
        self.assertEqual(s.instance.provider_contact_set.all()[1].for_orders, False)


class OrganizationTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "Organization"
        }
        s = OrganizationSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Organization")
        self.organizations = [s.instance]

    def test_edit(self):
        data = {
            "id": self.organizations[0].id,
            "name": "new name"
        }
        s = OrganizationSerializer(self.organizations[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "new name")
        self.assertEqual(s.instance.id, self.organizations[0].id)


class OrderTestCase(TestCase):

    def setUp(self):
        s = ProductSerializer(data=ProductTestCase.PRODUCTS_DATA, many=True)
        s.is_valid()
        s.save()
        self.products = s.instance
        s = OrganizationSerializer(data={"name":"Storage1"})
        s.is_valid()
        s.save()
        self.organization = s.instance
        s = OrganizationStorageSerializer(data={
            "organization":self.organization.id,
            "storage_type":"Stock"
            })
        s.is_valid()
        s.save()
        self.organization_storage = s.instance
        data = {
            "name": "Provider"
        }
        s = ProviderSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Provider")
        self.providers = [s.instance]

    def test_order_create(self):
        data = {
            "organization_storage": self.organization_storage.id,
            "provider": self.providers[0].id,
            "order_product_set": json.dumps([{
                "product": self.products[0].id,
                "amount": 5
            }])
        }
        s = OrderSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertGreaterEqual(s.instance.id, 1)
        self.assertEqual(s.instance.status, Order.STATUS_PENDING)

class InvoiceTestCase(TestCase):

    def setUp(self):
        data = {
            "name": "Provider"
        }
        s = ProviderSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.name, "Provider")
        self.providers = [s.instance]
        data = {
            "date": "2018-10-05",
            "number": "0000",
            "provider": self.providers[0].id
        }
        s = InvoiceSerializer(data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertGreaterEqual(s.instance.id, 1)
        self.assertEqual(s.instance.price, 0)
        data["price"] = 500
        s = InvoiceSerializer(s.instance, data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.number, "0000")
        self.assertEqual(s.instance.price, 500)
        self.invoices = [s.instance]

    def test_add_payment(self):
        data = {
            "id": self.invoices[0].id,
            "payment_set": json.dumps([
                {
                    'date': '2018-10-06',
                    'amount': 100
                },
                {
                    'date': '2018-10-07',
                    'amount': 50.5
                }
            ])
        }
        s = InvoiceSerializer(self.invoices[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.price, 500)
        self.assertEqual(s.instance.paid, False)
        self.assertEqual(s.instance.id, self.invoices[0].id)
        data = {
            "id": self.invoices[0].id,
            "payment_set": json.dumps([
                {
                    'date': '2018-10-06',
                    'amount': 100
                },
                {
                    'date': '2018-10-07',
                    'amount': 50.5
                },
                {
                    'date': '2018-10-08',
                    'amount': 349.5
                }
            ])
        }
        s = InvoiceSerializer(self.invoices[0], data=data)
        self.assertTrue(s.is_valid())
        s.save()
        self.assertEqual(s.instance.price, 500)
        self.assertEqual(s.instance.paid, True)
        self.assertEqual(s.instance.id, self.invoices[0].id)