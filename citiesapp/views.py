import json

from django.core import serializers
from django.http import HttpResponse
from django.shortcuts import render

from citiesapp.models import State, City


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
            print(valores)
        except:
            valores = 0
    return HttpResponse(json.dumps(valores), content_type='application/json')
