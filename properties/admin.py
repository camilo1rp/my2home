from django.contrib import admin
from properties.models import Property, AddressCol, BusinessType, Image, Contact, Facility

# admin.site.register(Property)
admin.site.register(AddressCol)
admin.site.register(BusinessType)
admin.site.register(Contact)
admin.site.register(Facility)
# admin.site.register(Image)

@admin.register(Property)
class PropertyAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'code', 'type_property', 'price_str', 'rooms', 'baths', 'created')
    list_filter = ('type_property', 'created')
    search_fields = ('code', 'type_property')

@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('propiedad', 'main', 'image')
