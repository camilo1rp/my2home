from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.utils.translation import gettext_lazy as _
from .forms import PropertyForm, AddressColForm, ImageForm
from .models import Property, AddressCol, Image
from django.forms import modelformset_factory

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
        self.new_property.manager = self.request.user
        self.new_property.save()
        return super(CreateProperty, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property:create-address', args=[self.new_property.id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 0
        return context

    # def get(self, request, *args, **kwargs):
    #     self.business = BusinessType.objects.all()
    #     return super().get(request, *args, **kwargs)
    #


class UpdateProperty(UpdateView):
    model = Property
    template_name = 'properties/new_property.html'
    form_class = PropertyForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page'] = 0
        return context

    def form_valid(self, form):
        self.new_property = form.save(commit=False)
        self.new_property.manager = self.request.user
        self.new_property.save()
        print(self.new_property.id)
        return super(UpdateProperty, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property:create-address', args=[self.new_property.id])

    # def get_object(self):
    #     return self.model.objects.get(pk=self.request.GET.get('pk'))


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
        if Property.objects.get(id=prop_id).address_col.all():
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(request.POST or None, instance=instance)
        else:
            form = AddressColForm()
    return render(request, 'properties/new_property.html', {'form': form, 'propiedad': prop_id, 'page': 1})


def create_image(request, prop_id=None):
    images_formset = modelformset_factory(Image, fields=['propiedad', 'image', 'main'], extra=2)
    if request.method == 'POST':
        form = images_formset(request.POST or None, request.FILES or None)
        print(form)
        if form.is_valid():
            prop = Property.objects.get(id=prop_id)
            for obj in form:
                _new_image = Image.objects.get_or_create(propiedad=prop, image=obj.cleaned_data['image'], main=obj.cleaned_data['main'])
            return HttpResponseRedirect(reverse('property:index', ))
    images_formset = images_formset(queryset=Image.objects.none())
    return render(request, 'properties/new_image.html', {'form': images_formset, 'propiedad': prop_id, 'page': 2})


def property_detail(request, prop_id):
    prop = get_object_or_404(Property, id=prop_id)
    return render(request, 'properties/property-details.html',
                  {'prop': prop})
