import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from database.models import *

import sqlite3
import mysql.connector
import sys

print("Migrating", sys.argv[1])

conn = sqlite3.connect(sys.argv[1])
c = conn.cursor()

try:
    c.execute('SELECT * FROM database_product;')
    for product in c.fetchall():
        print(product[0])
        p = Product.objects.get(code=product[0])
        st = StorageType.objects.get(name="Consignacion")
        os = Organization_Storage.objects.get(storage_type=st)
        s = Storage_Product.objects.get(product=p, organization_storage=os)
        s.amount = int(product[4])
        s.save()
        st = StorageType.objects.get(name="Propias")
        os = Organization_Storage.objects.get(storage_type=st)
        s = Storage_Product.objects.get(product=p, organization_storage=os)
        s.amount = int(product[6])
        s.save()
        st = StorageType.objects.get(name="Obsoletas")
        os = Organization_Storage.objects.get(storage_type=st)
        s = Storage_Product.objects.get(product=p, organization_storage=os)
        s.amount = int(product[7])
        s.save()
except Exception as e:
    print(e)
    import pdb; pdb.set_trace()
