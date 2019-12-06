from django.shortcuts import render
from django.views.generic import ListView

from .models import Property


class CreateProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 6


def index(request):
    return render(request, 'properties/index.html', )
