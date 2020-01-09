import csv
import io
import json
import urllib
from email.mime.image import MIMEImage
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView

from visits.visits import Visits
from .forms import PropertyForm, AddressColForm, ContactForm, MultiPropForm
from .models import Property, AddressCol, Image, Contact, BusinessType


class ListProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 12
    def get(self, request, *args, **kwargs):
        property_type = request.GET.get('list-types')
        business_type = request.GET.get('offer-types')
        city = request.GET.get('select-city')
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


def create_address(request, prop_id=30):# //TODO: ************ CAMBIAR PROPIEDAD a None***************
    if request.method == 'POST':
        if Property.objects.get(id=prop_id).address_col.all(): # check if property has address
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(instance=instance, data=request.POST)
        else:
            form = AddressColForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.save()
            return HttpResponseRedirect(reverse('property:create-image', args=(new_address.propiedad.id,)))
        print("error")
    else:
        if Property.objects.get(id=prop_id).address_col.all():
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(request.POST or None, instance=instance)
        else:
            form = AddressColForm()
    return render(request, 'properties/new_property.html', {'form': form, 'propiedad': prop_id, 'page': 1})


def create_image(request, prop_id=None):
    images_formset = modelformset_factory(Image, fields=['image', 'main'], extra=6)
    if request.method == 'POST':
        form = images_formset(request.POST or None, request.FILES or None)
        if form.is_valid():
            prop1 = request.POST.get('propiedad_id')
            print(prop1)
            prop = Property.objects.get(id=int(prop_id))
            for obj in form:
                try:
                    img_in = obj.cleaned_data['image']
                    main_in = obj.cleaned_data['main']                   
                    _new_image = Image.objects.get_or_create(propiedad=prop,
                                                             image=img_in,
                                                             main=main_in)
                except KeyError:
                    continue
            return HttpResponseRedirect(reverse('property:index', ))
    images_formset = images_formset(queryset=Image.objects.none())
    return render(request, 'properties/new_property.html', {'form': images_formset, 'propiedad': prop_id, 'page': 2})


def property_detail(request, prop_id):
    prop = get_object_or_404(Property, id=prop_id)
    visit = Visits(request)
    visit.add(prop_id)
    if request.method == 'POST':
        print("request post")
        form = ContactForm(request.POST)
        if form.is_valid():
            print("valid form")
            name_in = form.cleaned_data['name']
            phone_in = form.cleaned_data['phone']
            try:
                email_in = form.cleaned_data['email']
            except KeyError:
                print("no email provided")
                email_in = 'noemail@nomail.com'
            contact, _ = Contact.objects.get_or_create(propiedad=prop, name=name_in, phone=phone_in, email=email_in)

            file = "/media/{}".format(prop.gallery.get(main=True).image)
            data = {'propiedad': contact.propiedad, 'name': contact.name, 'phone': contact.phone,
                    'email': contact.email, 'image':file}
            html_content = render_to_string('properties/contact_email.html', {'data': data})
            subject = '{} esta interesad@ en la propiedad: {} - {}'.format(data['name'].title(),
                                                                           data['propiedad'].title,
                                                                           data['propiedad'].code)
            msg = EmailMultiAlternatives(subject, html_content, 'camilo1rp@gmail.com', ['camilo1rp@gmail.com'])
            msg.content_subtype = "html"
            msg.mixed_subtype = "related"
            print(file[1::])
            img = open(file[1::], 'rb').read()
            url = file
            image = MIMEImage(img, 'jpg')
            image.add_header('Content-ID', '<{}>'.format(url))
            image.add_header("Content-Disposition", "inline", filename=url)
            msg.attach(image)
            msg.send()
            message = _('Your information has been sent to our agents! Thank you')
            print("email_sent")
            return render(request, 'properties/property-details.html',
                          {'prop': prop, 'mess': message, })
        else:
            return HttpResponse("error submiting file")

    form = ContactForm()
    return render(request, 'properties/property-details.html',
                  {'prop': prop, 'form': form})


def whatsapp_contact(request, prop_id, phone=3162128561):
    prop = get_object_or_404(Property, id=prop_id)
    message = _("I am interested in the property: {}, Address: {}, code: {}. Is it still Available")\
        .format(prop.title, prop.address_col.get(), prop.code)
    print('message: {}'.format(message))
    phone_str = str(phone)
    message_parsed = urllib.parse.quote(message)
    print('message parsed: {}'.format(message_parsed))
    whatsapp_url = "https://wa.me/57{}?text={}".format(phone_str, message_parsed)
    print('url:{}'.format(whatsapp_url))
    return redirect(whatsapp_url)


# send_email(new_contact)
# //TODO: move email from property_detail to a funtion in tasks.py after setting up Celery

class Tyc(TemplateView):
    template_name = "properties/tyc.html"


def property_upload(request):
    template = 'properties/upload.html'
    if request.method == 'POST':
        form = MultiPropForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            csv_file = form.cleaned_data['csv_file']
            owner = form.cleaned_data['owner']
            manager = request.user
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be format:  .CVS')
                print("file error")
                return redirect(reverse('gestores:producto-upload'))
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            property_data = csv.reader(io_string, delimiter=",", quotechar="|")
            for column in property_data:
                if not Property.objects.filter(upload_code=column[13]):
                    print( "**** NEW PROPERTY ****")
                    prop, _ = Property.objects.get_or_create(manager=manager, owner=owner, type_property=column[0],
                                                  price=column[1], price_str=column[2], rooms=column[3],
                                                  baths=column[4], parking=column[5], area_built=column[6],
                                                  area_total=column[7], estrato=column[8], year=column[9],
                                                  title=column[10], description=column[11], upload_code=column[13])
                else:
                    print( "**** ALTER PROPERTY ****")
                    prop = Property.objects.get(upload_code=column[13])
                    prop.__dict__.update(manager=manager, owner=owner, type_property=column[0],
                                                  price=column[1], price_str=column[2], rooms=column[3],
                                                  baths=column[4], parking=column[5], area_built=column[6],
                                                  area_total=column[7], estrato=column[8], year=column[9],
                                                  title=column[10], description=column[11],)
                prop.save()
                types = column[12].split('-')
                for typ in types:
                    t = typ.lower()
                    if t == 'arriendo' or t == 'arrendamiento' or t == 'arrendar':
                        value = 'RENT / ARRENDAMIENTO'
                    elif t == 'permuta' or t == 'permutar' or t == 'permuto':
                        value = 'SWAP / PERMUTA'
                    elif t == 'venta' or t == 'vender' or t == 'vendo':
                        value = 'SALE / VENTA'
                    else:
                        value = 'SALE / VENTA'
                    business = BusinessType.objects.get(name=value)
                    prop.type_business.add(business)
                    prop.save()
                return HttpResponseRedirect(reverse('property:index'))
    form = MultiPropForm()
    return render(request, template, {'form': form})