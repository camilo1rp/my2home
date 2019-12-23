from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView
from django.utils.translation import gettext_lazy as _
from .forms import PropertyForm, AddressColForm, ImageForm
from .models import Property, AddressCol, Image


class ListProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        property_type = request.GET.get('list-types')
        print(property_type)
        business_type = request.GET.get('offer-types')
        print(business_type)
        city = request.GET.get('select-city')
        print(city)
        filters = {}
        if property_type == business_type and business_type == city:
            self.object_list = self.model.objects.all()
            context = self.get_context_data()
            context['pro_section'] = False
        else:
            if property_type != 'ALL':
                filters['type_property'] = property_type
            if business_type != 'ALL':
                filters['type_business__name'] = business_type
            query = Property.objects.filter(**filters)
            if city != 'ALL':
                prop_with_address = [prop for prop in query if prop.address_col.all()]
                query = [q for q in prop_with_address if q.address_col.get().ciudad == city]
            self.object_list = query
            context = self.get_context_data()
            context['pro_section'] = True
        return self.render_to_response(context)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 0
        return context

    # def get(self, request, *args, **kwargs):
    #     self.business = BusinessType.objects.all()
    #     return super().get(request, *args, **kwargs)
    #



def create_address(request, prop_id=None):
    if request.method == 'POST':
        form = AddressColForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            if Property.objects.get(id=prop_id).address_col.all():
                return render(request, 'properties/new_address_col.html',
                              {'form': form,
                               'error': _('address already added to property')})
            new_address.save()
            property_id = new_address.propiedad.id
            return HttpResponseRedirect(reverse('property:create-image', args=(property_id,)))
    else:
        form = AddressColForm()
    return render(request, 'properties/new_property.html', {'form': form, 'propiedad': prop_id, 'page': 1})


def create_image(request, prop_id=None):
    if request.method == 'POST':
        form = ImageForm(request.POST, request.FILES)
        if form.is_valid():
            image = request.FILES['image']
            prop = Property.objects.get(id=prop_id)
            _new_image = Image.objects.get_or_create(propiedad=prop, image=image)
            return HttpResponseRedirect(reverse('property:index',))
    else:
        form = ImageForm()
    return render(request, 'properties/new_image.html', {'form': form, 'propiedad': prop_id, 'page': 2})
