from django.contrib.auth.decorators import login_required
import json
from django.http import HttpResponse
from django.shortcuts import render
from properties.models import Property, Contact


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

def messages(request):
    user = request.user
    props = user.my_properties.all()  # get user's properties
    messages = [prop.contacts.all() for prop in props if len(prop.contacts.all()) > 0]  # get contacts for all user's properties with messages
    return render(request, 'properties/messages_list.html', {'messages': messages})

@login_required
def message_detail(request, mess_id):
    message = Contact.objects.get(id=mess_id)
    if request.method == 'POST':
        message.delete()
        return HttpResponse(json.dumps(1), content_type='application/json')
    return render(request, 'properties/message_details.html', {'mess': message})