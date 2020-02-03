from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from properties.models import Property


@login_required
def dashboard(request):
    user = request.user
    return render(request, 'account/dashboard.html', {'user': user})


def property_card(request):
    user = request.user
    properties = Property.objects.filter(manager=user)
    return render(request, 'properties/property_card_scroll.html', {'properties': properties,
                                                                    'editable': True})


def favorite_card(request):
    user = request.user
    following = user.rel_from_set.all()
    properties = [prop.property_followed for prop in following]
    return render(request, 'properties/property_card_scroll.html', {'properties': properties})