from django import template
from properties.models import AddressCol, Property

register = template.Library()


@register.inclusion_tag('properties/property_card.html')
def show_latest_properties(count=5, city="a", prop_id=0):
    print(city)
    address_city = AddressCol.objects.filter(ciudad=city).order_by('-id')
    properties_city = [address.propiedad for address in address_city if address.propiedad.id != prop_id]
    if not properties_city:
        latest_properties = Property.objects.order_by('-created').exclude(id=prop_id)[:count]
    else:
        latest_properties = properties_city[:count]
    return {'properties': latest_properties}
