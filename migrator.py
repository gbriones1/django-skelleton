import sqlite3
import mysql.connector
import sys

print("Migrating", sys.argv[1])

providers = {}
brands = {}
appliances = {}
products = {}
organizations = {}

storagetype_ids = {}
duraznera_storage_ids = {}

cnx = mysql.connector.connect(user='root', password='pass', database='django_test_2')
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
    c.execute('SELECT * FROM database_percentage;')
    for pr in c.fetchall():
        query = 'INSERT INTO warehouse_percentage (max_price_limit, percentage_1, percentage_2, percentage_3) VALUES ({}, {}, {}, {})'.format(pr[1], pr[2], pr[3], pr[4])
        cursor.execute(query)

    for st in ['Consignacion', 'Propias', 'Obsoletas']:
        query = 'INSERT INTO warehouse_storagetype (name) VALUES ("{}")'.format(st)
        # print query
        cursor.execute(query)
        storagetype_ids[st] = cursor.lastrowid
    c.execute('SELECT * FROM database_organization;')
    for org in c.fetchall():
        query = 'INSERT INTO warehouse_organization (name) VALUES ("{}")'.format(org[1])
        # print query
        cursor.execute(query)
        organizations[org[0]] = {"name": org[1], "new_id":cursor.lastrowid}
        if org[1] == "DURAZNERA":
            for st in storagetype_ids.keys():
                query = 'INSERT INTO warehouse_organization_storage (organization_id, storage_type_id) VALUES ({}, {})'.format(organizations[org[0]]["new_id"], storagetype_ids[st])
                # print query
                cursor.execute(query)
                duraznera_storage_ids[st] = cursor.lastrowid


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
        else:
            # product_values = '("{code}", "{name}", "{description}", {price}, {discount}, {provider}, {brand})'.format(**products[pk])
            # query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id) VALUES "+product_values
            # print query
            # cursor.execute(query)
            product_values = '(%(code)s, %(name)s, %(description)s, %(price)s, %(discount)s, %(provider)s, %(brand)s)'
            query = "INSERT INTO warehouse_product (code, name, description, price, discount, provider_id, brand_id) VALUES "+product_values
        cursor.execute(query, products[pk])
        products[pk]["new_id"] = cursor.lastrowid
        query = 'INSERT INTO warehouse_storage_product (amount, organization_storage_id, product_id, must_have) VALUES ({}, {}, {}, {})'.format(product[4], duraznera_storage_ids["Consignacion"], products[pk]["new_id"], product[8])
        cursor.execute(query)
        query = 'INSERT INTO warehouse_storage_product (amount, organization_storage_id, product_id, must_have) VALUES ({}, {}, {}, {})'.format(product[6], duraznera_storage_ids["Propias"], products[pk]["new_id"], product[9])
        cursor.execute(query)
        query = 'INSERT INTO warehouse_storage_product (amount, organization_storage_id, product_id, must_have) VALUES ({}, {}, {}, NULL)'.format(product[7], duraznera_storage_ids["Obsoletas"], products[pk]["new_id"])
        cursor.execute(query)

    c.execute('SELECT * FROM database_input;')
    for inp in c.fetchall():
        old_input_id = inp[0]
        storage_id = duraznera_storage_ids["Consignacion"]
        if inp[2] == 'S':
            storage_id = duraznera_storage_ids["Propias"]
        query = 'INSERT INTO warehouse_movement (date, organization_storage_id) VALUES ("{}", {})'.format(inp[1], storage_id)
        print query
        cursor.execute(query)
        movement_id = cursor.lastrowid
        invoice_number = '"{}"'.format(inp[3]) if inp[3] else 'NULL'
        query = 'INSERT INTO warehouse_input (invoice_number, movement_id) VALUES ({}, {})'.format(invoice_number, movement_id)
        print query
        cursor.execute(query)
        input_id = cursor.lastrowid
        c.execute('SELECT * FROM database_input_product WHERE input_reg_id = {}'.format(old_input_id))
        for reg in c.fetchall():
            query = 'INSERT INTO warehouse_input_product (amount, price, input_reg_id, product_id) VALUES ({},{},{},{})'.format(reg[1], reg[4], input_id, products[reg[2]]["new_id"])
            print query
            cursor.execute(query)

    c.execute('SELECT * FROM database_output;')
    for outp in c.fetchall():
        old_output_id = outp[0]
        storage_id = duraznera_storage_ids["Consignacion"]
        if outp[2] == 'S':
            storage_id = duraznera_storage_ids["Propias"]
        query = 'INSERT INTO warehouse_movement (date, organization_storage_id) VALUES ("{}", {})'.format(outp[1], storage_id)
        print query
        cursor.execute(query)
        movement_id = cursor.lastrowid
        replacer_id = organizations[outp[5]]["new_id"] if outp[5] else 'NULL'
        query = 'INSERT INTO warehouse_output (employee, destination, movement_id, replacer_id) VALUES ("{}", "{}", {}, {})'.format(outp[4], outp[3].encode("utf-8"), movement_id, replacer_id)
        print query
        cursor.execute(query)
        output_id = cursor.lastrowid
        c.execute('SELECT * FROM database_output_product WHERE output_reg_id = {}'.format(old_output_id))
        for reg in c.fetchall():
            query = 'INSERT INTO warehouse_output_product (amount, price, output_reg_id, product_id) VALUES ({},{},{},{})'.format(reg[1], reg[4], output_id, products[reg[2]]["new_id"])
            print query
            cursor.execute(query)

    cnx.commit()
except Exception as e:
    print e
    import pdb; pdb.set_trace()
    cnx.rollback()

cursor.close()

conn.close()
cnx.close()
