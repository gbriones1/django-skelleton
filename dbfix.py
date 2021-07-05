import os
import pdb
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")
import django
django.setup()

from database.models import *

for org_sto in Organization_Storage.objects.all():
    prod_set = set()
    for sp in Storage_Product.objects.filter(organization_storage=org_sto):
        if sp.product.code in prod_set:
            print(f"Repeated: {org_sto.id}, {sp.product.code}")
            sp.delete()
        else:
            prod_set.add(sp.product.code)

