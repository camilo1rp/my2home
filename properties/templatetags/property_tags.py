from django import template
from properties.models import AddressCol, Property

register = template.Library()


# @register.inclusion_tag('properties/property_card.html')
# def show_latest_properties(count=5, city=None):
#     address_city = AddressCol.objects.filter(ciudad=city)
#     if not address_city:
#         latest_properties = Property.objects.order_by('-created')[:count]
#     else:
#         properties_city = [address.propiedad for address in address_city]
#
#     latest_properties = Property.objects.filter(propertyorder_by('-created')[:count]
#     return {'properties': latest_properties}
