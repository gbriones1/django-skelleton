import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from database.models import *

import sqlite3
import mysql.connector
import sys

from datetime import datetime

print("Migrating", sys.argv[1])

providers = {}
brands = {}
appliances = {}
products = {}
organizations = {}

organization_storage = {}

storagetype_ids = {}
duraznera_storage_ids = {}

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

try:
    c.execute('SELECT * FROM database_provider;')
    for provider in c.fetchall():
        print(provider)
        pk = int(provider[0])
        p, created = Provider.objects.get_or_create(name=provider[1])
        providers[pk] = {'name':provider[1], 'email':provider[2], 'object':p}
        pc = Provider_Contact(name='Pedidos '+provider[1], department='Ventas', email=provider[2], provider=p, for_orders=True)
        pc.save()
    c.execute('SELECT * FROM database_brand;')
    for brand in c.fetchall():
        print(brand)
        pk = int(brand[0])
        brands[pk] = {'name':brand[1]}
        Brand.objects.get_or_create(name=brand[1])
    c.execute('SELECT * FROM database_appliance;')
    for appliance in c.fetchall():
        print(appliance)
        pk = int(appliance[0])
        appliances[pk] = {'name':appliance[1]}
        Appliance.objects.get_or_create(name=appliance[1])
    c.execute('SELECT * FROM database_percentage;')
    for pr in c.fetchall():
        print(pr)
        Percentage.objects.get_or_create(max_price_limit=pr[1], sale_percentage_1=pr[2], sale_percentage_2=pr[3], sale_percentage_3=pr[4], service_percentage_1=100, service_percentage_2=100, service_percentage_3=100)
    for st in ['Consignacion', 'Propias', 'Obsoletas']:
        print(st)
        StorageType.objects.get_or_create(name=st)
    c.execute('SELECT * FROM database_organization;')
    for org in c.fetchall():
        print(org)
        organization, created = Organization.objects.get_or_create(name=org[1])
        organizations[org[0]] = {"name": org[1], "object":organization}
        if org[1] == "DURAZNERA":
            for st in StorageType.objects.all():
                org_st, created = Organization_Storage.objects.get_or_create(organization=organization, storage_type=st)
                print(org_st)
                organization_storage[st.name] = org_st
    c.execute('SELECT database_product.*, database_product_appliance.appliance_id FROM database_product LEFT JOIN database_product_appliance ON database_product_appliance.product_id = database_product.code;')
    for product in c.fetchall():
        pk = product[0]
        products[pk] = {}
        products[pk]["code"] = product[0]
        products[pk]["name"] = product[1].encode("utf-8")
        products[pk]["description"] = product[2].encode("utf-8")
        products[pk]["price"] = product[3]
        products[pk]["discount"] = product[11]
        print(products[pk])
        appliance = None
        if product[12]:
            appliance = Appliance.objects.filter(name=appliances.get(int(product[12]))["name"]).first()
        p, created = Product.objects.get_or_create(
            code=product[0],
            name=product[1].encode("utf-8"),
            description=product[2].encode("utf-8"),
            price=float(product[3]),
            discount=product[11],
            provider=Provider.objects.get(name=providers[int(product[5])]["name"]),
            brand=Brand.objects.get(name=brands[int(product[10])]["name"]),
            appliance=appliance
        )
        products[pk]["object"] = p
        Storage_Product.objects.get_or_create(organization_storage=organization_storage["Consignacion"], product=p, amount=int(product[4]), must_have=int(product[8]))
        Storage_Product.objects.get_or_create(organization_storage=organization_storage["Propias"], product=p, amount=int(product[6]), must_have=int(product[9]))
        Storage_Product.objects.get_or_create(organization_storage=organization_storage["Obsoletas"], product=p, amount=int(product[7]))
    c.execute('SELECT * FROM database_order;')
    for order in c.fetchall():
        print(order)
        c.execute('SELECT * FROM database_order_product WHERE order_id = {}'.format(order[0]))
        prods = c.fetchall()
        if prods:
            provider = None
            claimant = None
            if order[3]:
                claimant, _ = Employee.objects.get_or_create(name=order[3])
            if order[2]:
                provider = providers[order[2]]["object"]
            org_sto = organization_storage["Consignacion"]
            if prods[0][5] == 'S':
                org_sto = organization_storage["Propias"]
            received_date = None
            if prods[0][6]:
                received_date = datetime.strptime(prods[0][6][:19], "%Y-%m-%d %H:%M:%S")
            order_new = Order(date=datetime.strptime(order[1][:19], "%Y-%m-%d %H:%M:%S"), organization_storage=org_sto, provider=provider, claimant=claimant, status=prods[0][7], received_date=received_date)
            order_new.save()
            for prod in prods:
                amount_received = int(prod[1])
                if prod[7] != "R":
                    amount_received = 0
                op = Order_Product(order=order_new, product=products[prod[3]]["object"], amount=int(prod[1]), amount_received=amount_received)
                op.save()
    c.execute('SELECT * FROM database_input;')
    for inp in c.fetchall():
        print(inp)
        c.execute('SELECT * FROM database_input_product WHERE input_reg_id = {}'.format(inp[0]))
        prods = c.fetchall()
        total_price = sum(map(lambda x: float(x[4]) * float(x[1]), prods))
        invoice = None
        if inp[3]:
            invoice = Invoice.objects.filter(number=inp[3], date=datetime.strptime(inp[1][:10], "%Y-%m-%d"))
            if invoice:
                invoice = invoice[0]
                invoice.price = float(invoice.price) + total_price
            else:
                provider = None
                if prods:
                    provider = products[prods[0][2]]["object"].provider
                invoice = Invoice(number=inp[3], date=datetime.strptime(inp[1][:10], "%Y-%m-%d"), price=total_price, provider=provider)
            invoice.save()
        org_sto = organization_storage["Consignacion"]
        if inp[2] == 'S':
            org_sto = organization_storage["Propias"]
        if invoice and Input.objects.filter(invoice=invoice):
            input_reg = Input.objects.get(invoice=invoice)
        else:
            input_reg = Input.objects.filter(date=datetime.strptime(inp[1][:19], "%Y-%m-%d %H:%M:%S"), organization_storage=org_sto, invoice=invoice)
            if input_reg:
                input_reg = input_reg[0]
            else:
                input_reg = Input(date=datetime.strptime(inp[1][:19], "%Y-%m-%d %H:%M:%S"), organization_storage=org_sto, invoice=invoice)
                input_reg.save()
        for prod in prods:
            mp = Movement_Product(movement=input_reg, product=products[prod[2]]["object"], amount=int(prod[1]), price=float(prod[4]))
            mp.save()
    c.execute('SELECT * FROM database_output;')
    for outp in c.fetchall():
        print(outp)
        c.execute('SELECT * FROM database_output_product WHERE output_reg_id = {}'.format(outp[0]))
        prods = c.fetchall()
        employee = None
        customer = None
        replacer = None
        if outp[4]:
            employee, _ = Employee.objects.get_or_create(name=outp[4])
        if outp[3]:
            customer, _  = Customer.objects.get_or_create(name=outp[3].encode("utf-8"))
        if outp[5]:
            replacer = organizations[outp[5]]["object"]
        org_sto = organization_storage["Consignacion"]
        if outp[2] == 'S':
            org_sto = organization_storage["Propias"]
        output_reg = Output.objects.filter(date=datetime.strptime(outp[1][:19], "%Y-%m-%d %H:%M:%S"), organization_storage=org_sto, employee=employee, destination=customer, replacer=replacer)
        if output_reg:
            output_reg = output_reg[0]
        else:
            output_reg = Output(date=datetime.strptime(outp[1][:19], "%Y-%m-%d %H:%M:%S"), organization_storage=org_sto, employee=employee, destination=customer, replacer=replacer)
            output_reg.save()
        for prod in prods:
            mp = Movement_Product(movement=output_reg, product=products[prod[2]]["object"], amount=int(prod[1]), price=float(prod[4]))
            mp.save()
except Exception as e:
    print(e)
    import pdb; pdb.set_trace()
