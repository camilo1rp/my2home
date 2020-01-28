import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from citiesapp.models import State, City
from properties.models import Property


def state(request):
    if request.is_ajax() and request.GET:
        id = request.GET.get("id")
        try:
            value = State.objects.filter(country_id=id).order_by('name')
            valores = serializers.serialize('json', value)
        except:
            valores = 0
    return HttpResponse(json.dumps(valores), content_type='application/json')


def city(request):
    if request.is_ajax() and request.GET:
        id_state = request.GET.get("id")
        try:
            value = City.objects.filter(state=id_state).order_by('name')
            valores = serializers.serialize('json', value)
        except:
            valores = 0
    return HttpResponse(json.dumps(valores), content_type='application/json')


def all_cities(request):
    if request.is_ajax():
        cities = [prop.address_col.get().ciudad.name for prop in Property.objects.all() if prop.address_col.all()]
        cities_distinct = list(set(cities))
        cities_sorted = cities_distinct.sort()
        dicta = dict(zip(cities_distinct, cities_distinct))
        print(dicta)
        try:
            valores = serializers.serialize('json', dicta)
        except:
            valores = 0
        print(valores)
    return HttpResponse(json.dumps(dicta), content_type='application/json')