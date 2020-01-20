import ast
import csv
import io
import json
import os
import urllib
import json
from email.mime.image import MIMEImage
from django.contrib import messages
from django.core.mail import EmailMultiAlternatives
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.translation import gettext_lazy as _t
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from geoservice.location import get_coordinates
from myhome import settings
from visits.visits import Visits
from .forms import PropertyForm, AddressColForm, ContactForm, MultiPropForm
from .models import Property, AddressCol, Image, Contact, BusinessType, Following


class ListProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 3

    def get(self, request, *args, **kwargs):
        # get data
        property_type = request.GET.get('list-types')
        business_type = request.GET.get('offer-types')
        city = request.GET.get('select-city')
        filters = request.GET.get('filters')
        # init variables
        filters_dict = {}
        query = self.model.objects.all()

        # check if there are filters
        if filters not in ['None', None]:
            filters_dict = ast.literal_eval(filters)
            query = self.model.objects.filter(**filters_dict)
        if property_type not in ['ALL', None, 'None']:
            filters_dict['type_property'] = property_type
        # else:
        #     filters_dict.pop('type_property', None)
        if business_type not in ['ALL', None, 'None']:
            filters_dict['type_business__name'] = business_type
        # else:
        #     filters_dict.pop('type_business__name', None)
        if filters_dict:
            query = self.model.objects.filter(**filters_dict)
        if city not in ['ALL', None]:
            prop_with_address = [prop for prop in query if prop.address_col.all()]
            query = [q for q in prop_with_address if q.address_col.get().ciudad == city]

        self.object_list = query

        if request.GET.get('prop_id'):
            try:
                user = self.request.user
                prop = Property.objects.get(id=request.GET.get('prop_id'))
            except:
                return HttpResponse(json.dumps(0), content_type='application/json')
            if user.following.filter(id=prop.id):
                user.following.remove(prop)
                user.save()
            else:
                follows = Following(user=user, property_followed=prop)
                follows.save()
        print(self.object_list)
        print(filters_dict)
        context = self.get_context_data()
        context['filters'] = filters_dict
        if request.is_ajax():
            return render(request, 'properties/property_list.html', context)
        return self.render_to_response(context)


def property_following(request):
    if request.method == 'GET':
        print(request.GET.get('prop_id'))
        all_properties = Property.objects.all()
        try:
            user = request.user
            prop = Property.objects.get(id=request.GET.get('prop_id'))
            print(prop)
        except:
            return HttpResponse(json.dumps(0), content_type='application/json')
        if user.following.filter(id=prop.id):
            user.following.remove(prop)
            user.save()
        else:
            follows = Following(user=user, property_followed=prop)
            follows.save()
        return render(request, 'properties/property_list.html', {'object_list': all_properties})


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
        return super(UpdateProperty, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('property:create-address', args=[self.new_property.id])

    # def get_object(self):
    #     return self.model.objects.get(pk=self.request.GET.get('pk'))


def create_address(request, prop_id=None):
    if request.method == 'POST':
        if Property.objects.get(id=prop_id).address_col.all():  # check if property has address
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(instance=instance, data=request.POST)
        else:
            form = AddressColForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.save()
            return HttpResponseRedirect(reverse('property:create-image', args=(new_address.propiedad.id,)))
    else:
        if Property.objects.get(id=prop_id).address_col.all():
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(request.POST or None, instance=instance)
        else:
            form = AddressColForm()
    return render(request, 'properties/new_property.html', {'form': form, 'propiedad': prop_id, 'page': 1})


def create_image(request, prop_id=None):
    prop = Property.objects.get(id=int(prop_id))
    images = prop.gallery.all()
    print(len(images))
    images_formset = modelformset_factory(Image, fields=['image', 'main'], extra=6-len(images))

    if request.method == 'POST':
        print('got posted')
        form = images_formset(request.POST or None, request.FILES or None)
        if form.is_valid():
            print('got valid')
            # prop1 = request.POST.get('propiedad_id')
            print(prop)
            for obj in form:
                print(obj.cleaned_data)
                try:
                    img_in = obj.cleaned_data['image']
                    main_in = obj.cleaned_data['main']
                    id_in = obj.cleaned_data['id']
                    if id_in is not None:
                        existing_image = Image.objects.get(id=obj.cleaned_data['id'].id)
                        if not img_in:
                            existing_image.delete()
                        else:
                            existing_image.image = img_in
                            existing_image.main = main_in
                            existing_image.save()
                    else:
                        _new_image = Image.objects.get_or_create(propiedad=prop,
                                                             image=img_in,
                                                             main=main_in)
                except KeyError:
                    continue
            return HttpResponseRedirect(reverse('property:index', ))
    if images:
        images_formset = images_formset(queryset=images)

    return render(request, 'properties/new_image2.html', {'form': images_formset, 'propiedad': prop_id, 'page': 2})


def property_detail(request, prop_id):
    prop = get_object_or_404(Property, id=prop_id)
    geo_data = get_coordinates(str(prop.address_col.get()))
    visit = Visits(request)
    visit.add(prop_id)
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name_in = form.cleaned_data['name']
            phone_in = form.cleaned_data['phone']
            try:
                email_in = form.cleaned_data['email']
            except KeyError:
                print("no email provided")
                email_in = 'noemail@nomail.com'
            contact, _ = Contact.objects.get_or_create(propiedad=prop, name=name_in, phone=phone_in, email=email_in)

            # ******** email sending ********
            # //TODO: move email from property_detail to a funtion in tasks.py after setting up Celery
            file = "/media/{}".format(prop.gallery.get(main=True).image)
            data = {'propiedad': contact.propiedad, 'name': contact.name, 'phone': contact.phone,
                    'email': contact.email, 'image': file}
            html_content = render_to_string('properties/contact_email.html', {'data': data})
            subject = '{} esta interesad@ en la propiedad: {} - {}'.format(data['name'].title(),
                                                                           data['propiedad'].title,
                                                                           data['propiedad'].code)
            msg = EmailMultiAlternatives(subject, html_content, 'camilo1rp@gmail.com', ['camilo1rp@gmail.com'])
            msg.content_subtype = "html"
            msg.mixed_subtype = "related"
            img = open(file[1::], 'rb').read()
            url = file
            image = MIMEImage(img, 'jpg')
            image.add_header('Content-ID', '<{}>'.format(url))
            image.add_header("Content-Disposition", "inline", filename=url)
            msg.attach(image)
            msg.send()
            message = _t('Your information has been sent to our agents! Thank you')
            print("email_sent")
            # ****************
            return render(request, 'properties/property-details.html',
                          {'prop': prop, 'mess': message,
                           'lat': geo_data["lat"], 'lng': geo_data["lng"]})
        else:
            return HttpResponse("error submiting file")
    form = ContactForm()
    return render(request, 'properties/property-details.html',
                  {'prop': prop, 'form': form, 'lat': geo_data["lat"],
                   'lng': geo_data["lng"]})


def whatsapp_contact(request):
    prop_id = request.GET.get('id')
    phone = 3162128561
    prop = get_object_or_404(Property, id=prop_id)
    message = "I am interested in the property: {}, Address: {}, code: {}. Is it still Available" \
        .format(prop.title, prop.address_col.get(), prop.code)
    print('message: {}'.format(message))
    phone_str = str(phone)
    message_parsed = urllib.parse.quote(message)
    print('message parsed: {}'.format(message_parsed))
    whatsapp_url = "https://wa.me/57{}?text={}".format(phone_str, message_parsed)
    print('url:{}'.format(whatsapp_url))
    return HttpResponse(json.dumps(whatsapp_url), content_type='application/json')


class Tyc(TemplateView):
    template_name = "properties/tyc.html"


def property_upload(request):
    template = 'properties/upload.html'
    if request.method == 'POST':
        form = MultiPropForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            # get form data
            csv_file = form.cleaned_data['csv_file']
            owner = form.cleaned_data['owner']
            # get user adding properties
            manager = request.user
            # get csv data
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'File must be format:  .CVS')
                print("file error")
                return redirect(reverse('gestores:producto-upload'))
            data_set = csv_file.read().decode('UTF-8')
            io_string = io.StringIO(data_set)
            next(io_string)
            property_data = csv.reader(io_string, delimiter=",", quotechar="|")
            # create property, address, images
            for column in property_data:
                # check if address is to be shown
                mostrar = False
                if column[23] in {'si', '1', 'mostrar', 1, }:
                    mostrar = True
                # check if property already exists
                if not Property.objects.filter(upload_code=column[13]):

                    # create property
                    prop, _ = Property.objects.get_or_create(manager=manager, owner=owner, type_property=column[0],
                                                             price=column[1], price_str=column[2], rooms=column[3],
                                                             baths=column[4], parking=column[5], area_built=column[6],
                                                             area_total=column[7], estrato=column[8], year=column[9],
                                                             title=column[10], description=column[11])
                    # create address
                    addr, _ = AddressCol.objects.get_or_create(propiedad=prop, tipo_via=column[14], via=column[15],
                                                               prefijo_via=column[16], numero=column[17],
                                                               prefijo_numero=column[18], placa=column[19],
                                                               barrio=column[20], ciudad=column[21],
                                                               departamento=column[22], mostrar=mostrar)
                else:
                    # get property
                    prop = Property.objects.get(upload_code=column[13])
                    # update property
                    prop.__dict__.update(manager=manager, owner=owner, type_property=column[0],
                                         price=column[1], price_str=column[2], rooms=column[3],
                                         baths=column[4], parking=column[5], area_built=column[6],
                                         area_total=column[7], estrato=column[8], year=column[9],
                                         title=column[10], description=column[11], )
                    # get address
                    addr = prop.address_col.get()
                    # update address
                    addr.__dict__.update(propiedad=prop, tipo_via=column[14], via=column[15],
                                         prefijo_via=column[16], numero=column[17],
                                         prefijo_numero=column[18], placa=column[19],
                                         mostrar=mostrar)
                prop.save()
                addr.save()
                # check the types of business and add them to property
                types = column[12].split('-')
                for typ in types:
                    t = typ.lower()
                    if t in {'arriendo', 'arrendamiento', 'arrendar'}:
                        value = 'RENT / ARRENDAMIENTO'
                    elif t in {'permuta', 'permutar', 'permuto'}:
                        value = 'SWAP / PERMUTA'
                    elif t in {'venta', 'vender', 'vendo'}:
                        value = 'SALE / VENTA'
                    else:
                        value = 'SALE / VENTA'
                    business = BusinessType.objects.get(name=value)
                    prop.type_business.add(business)
                # get images from folder
                images = [column[24] + '/' + img for img in os.listdir(settings.MEDIA_ROOT + column[24] + '/')
                          if img.endswith("jpg") or img.endswith("png")]
                # save images for propery and make the first image the main one
                main = True
                for image in images:
                    img = Image(propiedad=prop, image=image, main=main)
                    img.save()
                    main = False

                prop.save()
            return HttpResponseRedirect(reverse('property:index'))
    form = MultiPropForm()
    return render(request, template, {'form': form})


def Template(request):
    prop = Property.objects.last()
    a = prop.address_col.get()
    geo_data = get_coordinates(str(a))
    template = 'properties/maps.html'
    data = {'propiedad': prop, 'name': "nombre apellido", 'phone': "1234456809",
            'email': "email@email.com", 'geo_data': geo_data}
    return render(request, template, {'data': data})
