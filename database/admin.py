from django.contrib import admin

from database.models import Product, Input

class ProductAdmin(admin.ModelAdmin):
    pass

class InputAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Input, InputAdmin)
