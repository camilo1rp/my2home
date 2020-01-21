from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from properties.models import Property

@login_required
def dashboard(request):
	return render(request, 'account/dashboard.html',)

def card(request):
	latest_properties = Property.objects.order_by('-created')
	return render(request, 'properties/property_card_scroll.html', {'properties': latest_properties})


