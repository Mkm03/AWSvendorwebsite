from django.contrib import admin
from .models import Vendor, Product, UserProfile

admin.site.register(Vendor)
admin.site.register(Product)
admin.site.register(UserProfile)