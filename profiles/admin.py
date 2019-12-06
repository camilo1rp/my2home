from django.contrib import admin

from properties.models import Property, addressCol

admin.site.register(Property)
admin.site.register(addressCol)