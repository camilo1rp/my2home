from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView

from .forms import PropertyForm, AddressColForm
from .models import Property, AddressCol


class ListProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 6


class CreateProperty(CreateView):
    model = Property
    template_name = 'properties/new_property.html'
    form_class = PropertyForm

    def form_valid(self, form):
        self.new_property = form.save(commit=False)
        self.new_property.save()
        print(self.new_property.id)
        return super(CreateProperty, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property:create-address',  args=[self.new_property.id])

    # def get(self, request, *args, **kwargs):
    #     self.business = BusinessType.objects.all()
    #     return super().get(request, *args, **kwargs)
    #
    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     context['business'] = self.business
    #     return context


def create_address(request, prop_id=None):
    if request.method == 'POST':
        form = AddressColForm(request.POST)
        if form.is_valid():
            new_address = form.save()
            property_id = new_address.propiedad.id
            return render(request, )
    else:
        form = AddressColForm()
    return render(request, 'properties/new_address_col.html', {'form': form, 'propiedad': prop_id})
