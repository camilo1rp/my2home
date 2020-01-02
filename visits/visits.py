from decimal import Decimal
from django.conf import settings
from django.shortcuts import get_object_or_404

from properties.models import Property


class Visits(object):
    def __init__(self, request):
        self.session = request.session
        visits = self.session.get(settings.VISITS_SESSION_ID)
        if not visits:
            # save an empty cart in the session
            visits = self.session[settings.VISITS_SESSION_ID] = {}
        self.visits = visits

    def add(self, property_id):
        prop_id = str(property_id)
        if prop_id not in self.visits:
            self.visits[prop_id] = {'visit': True}
            prop = get_object_or_404(Property, id=property_id)
            prop.seen += 1
            prop.save()
            print("visit registerd")
        else:
            print("property page already visit")
        self.save()

    def save(self):
        self.session.modified = True
