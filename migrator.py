import sqlite3
import mysql.connector
import sys

print("Migrating", sys.argv[1])

providers = {}
brands = {}
appliances = {}
products = {}

cnx = mysql.connector.connect(user='root', password='pass', database='django_test')
cursor = cnx.cursor()

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

try:
    c.execute('SELECT * FROM database_provider;')
    for provider in c.fetchall():
        print provider
        pk = int(provider[0])
        providers[pk] = {'name':provider[1], 'email':provider[2]}
        # query = 'INSERT INTO warehouse_provider (name, email) VALUES ("{name}", "{email}")'.format(**providers[pk])
        # print query
        # cursor.execute(query)
        query = 'INSERT INTO warehouse_provider (name, email) VALUES (%(name)s, %(email)s)'
        cursor.execute(query, providers[pk])
        providers[pk]['new_id'] = cursor.lastrowid
    c.execute('SELECT * FROM database_brand;')
    for brand in c.fetchall():
        print brand
        pk = int(brand[0])
        brands[pk] = {'name':brand[1]}
        # query = 'INSERT INTO warehouse_brand (name) VALUES ("{name}")'.format(**brands[pk])
        # print query
        # cursor.execute(query)
        query = 'INSERT INTO warehouse_brand (name) VALUES (%(name)s)'
        cursor.execute(query, brands[pk])
        brands[pk]['new_id'] = cursor.lastrowid
    c.execute('SELECT * FROM database_appliance;')
    for appliance in c.fetchall():
        print appliance
        pk = int(appliance[0])
        appliances[pk] = {'name':appliance[1]}
        # query = 'INSERT INTO warehouse_appliance (name) VALUES ("{name}")'.format(**appliances[pk])
        # print query
        # cursor.execute(query)
        query = 'INSERT INTO warehouse_appliance (name) VALUES (%(name)s)'
        cursor.execute(query, appliances[pk])
        appliances[pk]['new_id'] = cursor.lastrowid
    c.execute('SELECT * FROM database_product_appliance;')
    for pa in c.fetchall():
        # print pa
        pk = int(pa[0])
        products[pa[1]] = {'appliance':appliances[int(pa[2])]["new_id"]}

    c.execute('SELECT * FROM database_product;')
    for product in c.fetchall():
        pk = product[0]
        if not pk in products.keys():
            products[pk] = {'appliance':''}
        products[pk]["code"] = product[0]
        products[pk]["name"] = product[1].encode("utf-8")
        products[pk]["description"] = product[2].encode("utf-8")
        products[pk]["price"] = product[3]
        products[pk]["discount"] = product[11]
        products[pk]["provider"] = providers[int(product[5])]["new_id"]
        products[pk]["brand"] = brands[int(product[10])]["new_id"]
        print products[pk]
        if products[pk]["appliance"]:
            # product_values = '("{code}", "{name}", "{description}", {price}, {discount}, {provider}, {brand}, {appliance})'.format(**products[pk])
            # query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id, appliance_id) VALUES "+product_values
            # print query
            # cursor.execute(query)
            product_values = '(%(code)s, %(name)s, %(description)s, %(price)s, %(discount)s, %(provider)s, %(brand)s, %(appliance)s)'
            query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id, appliance_id) VALUES "+product_values
            cursor.execute(query, products[pk])
        else:
            # product_values = '("{code}", "{name}", "{description}", {price}, {discount}, {provider}, {brand})'.format(**products[pk])
            # query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id) VALUES "+product_values
            # print query
            # cursor.execute(query)
            product_values = '(%(code)s, %(name)s, %(description)s, %(price)s, %(discount)s, %(provider)s, %(brand)s)'
            query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id) VALUES "+product_values
            cursor.execute(query, products[pk])

    cnx.commit()
except Exception as e:
    import pdb; pdb.set_trace()
    cnx.rollback()

cursor.close()

conn.close()
cnx.close()
