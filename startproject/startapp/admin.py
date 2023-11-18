from django.contrib import admin
from startapp.models import Product,Cart,Buy
admin.site.register(Product)
# Register your models here.
admin.site.register(Cart)
admin.site.register(Buy)