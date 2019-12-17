from django.contrib import admin
from properties.models import Property, AddressCol, BusinessType, Image

admin.site.register(Property)
admin.site.register(AddressCol)
admin.site.register(BusinessType)
admin.site.register(Image)