from django import template
from properties.models import AddressCol, Property

register = template.Library()


@register.inclusion_tag('properties/property_card.html')
def show_latest_properties(count=6, city="a", prop_id=0):
    print(city)
    address_city = AddressCol.objects.filter(ciudad=city).order_by('-id')
    properties_city = [address.propiedad for address in address_city if address.propiedad.id != prop_id]
    if not properties_city:
        latest_properties = Property.objects.order_by('-created').exclude(id=prop_id)[:count]
    else:
        latest_properties = properties_city[:count]
    return {'properties': latest_properties}


@register.inclusion_tag('properties/property_card.html')  # for testing dashboard only
def show_properties(count=6):
    latest_properties = Property.objects.order_by('-created')[:count]
    return {'properties': latest_properties}


# returns the url of the current location with requests
@register.simple_tag(takes_context=True)
def query_transform(context, **kwargs):
    query = context['request'].GET.copy()
    for k, v in kwargs.items():
        query[k] = v
    return query.urlencode()


@register.filter
def get_item(dictionary, key):
    return dictionary.get(key)


@register.inclusion_tag('properties/maps.html')
def google_maps(lat, lng, show):
    print("inside function")
    return {'lat': lat, 'lng': lng, 'show': show}


@register.inclusion_tag('properties/property_carousel.html')
def show_promoted_props(count=3, city=None, ):
    properties_city = []
    if city is not None:
        address_city = AddressCol.objects.filter(ciudad=city).order_by('-id')
        properties_city = [address.propiedad for address in address_city if address.propiedad.promoted]
    if not properties_city:
        promoted_properties = Property.objects.order_by('-created')
    else:
        promoted_properties = properties_city[:count]
    return {'properties': promoted_properties}
