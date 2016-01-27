from django.contrib import admin

from warehouse.models import Product, Input_Product, Input

class ProductAdmin(admin.ModelAdmin):
    pass

class InputProductAdmin(admin.ModelAdmin):
    pass

class InputAdmin(admin.ModelAdmin):
    pass

admin.site.register(Product, ProductAdmin)
admin.site.register(Input_Product, InputProductAdmin)
admin.site.register(Input, InputAdmin)
