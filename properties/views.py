import ast
import csv
import io
import json
import os
import urllib
import json
from email.mime.image import MIMEImage
from smtplib import SMTPAuthenticationError

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives, send_mail
from django.forms import modelformset_factory
from django.http import HttpResponseRedirect, HttpResponse, JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic.base import TemplateView
from geoservice.location import get_coordinates
from myhome import settings
from visits.visits import Visits
from .decorators import user_is_propertys_manager
from .forms import PropertyForm, AddressColForm, ContactForm, MultiPropForm
from .models import Property, AddressCol, Image, Contact, BusinessType, Following


class ListProperty(ListView):
    model = Property
    template_name = 'properties/index.html'
    paginate_by = 6

    def get(self, request, *args, **kwargs):
        # get data
        current_filters = request.GET.get('current_filters')
        filter_index = request.GET.get('remove')
        city = request.GET.get('select-city')
        follow = request.GET.get('follow')
        filters_names = ['City', 'type_property', 'type_business__name', 'rooms__gte', 'rooms__lte', 'baths__gte',
                         'baths__lte', 'area_total__gte', 'area_total__lte', 'price__gte', 'price__lte', ]
        filters_values = [request.GET.get('select-city'), request.GET.get('list-types'), request.GET.get('offer-types'),
                          request.GET.get('room_min'),
                          request.GET.get('room_max'), request.GET.get('bath_min'), request.GET.get('bath_max'),
                          request.GET.get('area_min'), request.GET.get('area_max'), request.GET.get('price_min'),
                          request.GET.get('price_max')]
        filters_labels = {'select-city': gettext('City'), 'SALE / VENTA': {gettext('Offer Type'): gettext('Sale')},
                          'RENT / ARRENDAMIENTO': {gettext('Offer Type'): gettext('Rent')},
                          'SWAP / PERMUTA': {gettext('Offer Type'): gettext('Swap')},
                          'APT': {gettext('Property type'): gettext('Apartment')},
                          'HOU': {gettext('Property type'): gettext('House')},
                          'LAN': {gettext('Property type'): gettext('Land')},
                          'COM': {gettext('Property type'): gettext('Commercial')},
                          'FAR': {gettext('Property type'): gettext('Farm')}, 'rooms__gte': gettext('Min rooms'),
                          'rooms__lte': gettext('Max rooms'), 'baths__gte': gettext('Min bathrooms'),
                          'baths__lte': gettext('Max bathrooms'), 'area_total__gte': gettext('Min area'),
                          'area_total__lte': gettext('Max area'), 'price__gte': gettext('Min price'),
                          'price__lte': gettext('Max price'),
                          }
        # init variables
        query = self.model.objects.all().filter(active=True, pause=False)
        filters_dict = {}

        if current_filters:
            filters_dict = ast.literal_eval(current_filters)
            filters_dict.pop(list(filters_dict.items())[int(filter_index)][0])
            if 'City' in filters_dict:
                city = filters_dict['City']

        # assign data to filters
        new_filters = dict(zip(filters_names, filters_values))
        for key, value in new_filters.items():
            if value not in ['ALL', None, 'None']:
                filters_dict[key] = value

        # check if following action, otherwise assign filters to query
        if follow not in ['None', None]:
            if request.GET.get('prop_id'):  # if prop_id in request. it means following property action
                prop = Property.objects.get(id=request.GET.get('prop_id'))
                if request.user.is_authenticated:
                    user = self.request.user
                    if user.following.filter(id=prop.id):
                        user.following.remove(prop)
                        user.save()
                        print("{} stopped following {}".format(user, prop))
                        return HttpResponse(json.dumps({'command': 0, 'prop_id': prop.id}),
                                            content_type='application/json')
                    elif user != prop.manager:
                        follows = Following(user=user, property_followed=prop)
                        follows.save()
                        print("{} started following {}".format(user, prop))
                        return HttpResponse(json.dumps({'command': 1, 'prop_id': prop.id}),
                                            content_type='application/json')
                    else:
                        print('user owns this property')
                        return HttpResponse(json.dumps({'command': 2, 'prop_id': prop.id}),
                                            content_type='application/json')
                else:
                    return HttpResponse(json.dumps({'command': -1, 'prop_id': -1}), content_type='application/json')

        elif filters_dict:
            filters_query = filters_dict.copy()
            filters_query.pop('City', None)
            query = self.model.objects.filter(**filters_query).filter(active=True, pause=False)

        # check location filter
        if city not in ['ALL', None]:
            prop_with_address = [prop for prop in query if prop.address_col.all()]
            query = [q for q in prop_with_address if q.address_col.get().ciudad.name == city]

        # assign labels
        filters_active = filters_dict.copy()
        for k, v in filters_dict.items():
            if v in filters_labels:
                filters_active.pop(k, None)
                filters_active[list(filters_labels[v].keys())[0]] = list(filters_labels[v].values())[0]
            elif k in filters_labels:
                filters_active[filters_labels[k]] = v
                filters_active.pop(k, None)

        # format price
        try:
            filters_active['Min price'] = "${:0,.0f}".format(int(filters_active['Min price'])).replace(',', '.')
        except KeyError:
            try:
                filters_active['Min precio'] = "${:0,.0f}".format(int(filters_active['Min precio'])).replace(',', '.')
            except KeyError:
                pass
        try:
            filters_active['Max price'] = "${:0,.0f}".format(int(filters_active['Max price'])).replace(',', '.')
        except KeyError:
            try:
                filters_active['Max precio'] = "${:0,.0f}".format(int(filters_active['Max precio'])).replace(',', '.')
            except KeyError:
                pass

        # format area
        try:
            filters_active['Min area'] = "{:0,.0f}m\u00b2".format(int(filters_active['Min area'])).replace(',', '.')
        except KeyError:
            try:
                filters_active['Min área'] = "{:0,.0f}m\u00b2".format(int(filters_active['Min área'])).replace(',', '.')
            except KeyError:
                pass
        try:
            filters_active['Max area'] = "{:0,.0f}m\u00b2".format(int(filters_active['Max area'])).replace(',', '.')
        except KeyError:
            try:
                filters_active['Max área'] = "{:0,.0f}m\u00b2".format(int(filters_active['Max área'])).replace(',', '.')
            except KeyError:
                pass

        # assign query and filters to context
        self.object_list = query
        context = self.get_context_data()
        context['filters'] = filters_dict
        context['filters_active'] = filters_active

        if not request.is_ajax():
            return self.render_to_response(context)
        return render(request, 'properties/property_list.html', context)


def property_following(request):
    if request.method == 'GET':
        print(request.GET.get('prop_id'))
        all_properties = Property.objects.all()
        try:
            user = request.user
            prop = Property.objects.get(id=request.GET.get('prop_id'))
        except:
            return HttpResponse(json.dumps(0), content_type='application/json')
        if user.following.filter(id=prop.id):
            user.following.remove(prop)
            user.save()
        else:
            follows = Following(user=user, property_followed=prop)
            follows.save()
        return render(request, 'properties/property_list.html', {'object_list': all_properties})


class CreateProperty(LoginRequiredMixin, CreateView):
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

    def get_initial(self):
        owner = User.objects.filter(is_superuser=True)[0]
        return {
            'owner': owner,
        }

    def dispatch(self, *args, **kwargs):
        return super(CreateProperty, self).dispatch(*args, **kwargs)
    # def get(self, request, *args, **kwargs):
    #     self.business = BusinessType.objects.all()
    #     return super().get(request, *args, **kwargs)
    #


class UpdateProperty(LoginRequiredMixin, UpdateView):
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

    @method_decorator(user_is_propertys_manager)
    def dispatch(self, *args, **kwargs):
        return super(UpdateProperty, self).dispatch(*args, **kwargs)

    # def get_object(self):
    #     return self.model.objects.get(pk=self.request.GET.get('pk'))


@login_required
def create_address(request, prop_id=None):
    try:
        prop = Property.objects.get(id=prop_id)
    except ObjectDoesNotExist:
        return HttpResponse(gettext("Property does not exist"))
    if request.user not in [prop.manager, prop.owner]:
        return HttpResponse(gettext("Access denied"))
    if request.method == 'POST':
        if prop.address_col.all():  # check if property has address
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(instance=instance, data=request.POST)
        else:
            form = AddressColForm(request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            new_address.save()
            return HttpResponseRedirect(reverse('property:create-image', args=(new_address.propiedad.id,)))
    else:
        if prop.address_col.all():
            instance = get_object_or_404(AddressCol, propiedad__id=prop_id)
            form = AddressColForm(request.POST or None, instance=instance)
        else:
            form = AddressColForm()
    return render(request, 'properties/new_property.html', {'form': form, 'propiedad': prop_id, 'page': 1})


@login_required
def create_image(request, prop_id=None):
    try:
        prop = Property.objects.get(id=prop_id)
    except ObjectDoesNotExist:
        return HttpResponse(gettext("Property does not exist"))
    if request.user not in [prop.manager, prop.owner]:
        return HttpResponse(gettext("Access denied, you don't own or manage this property"))
    images = prop.gallery.all()
    images_formset = modelformset_factory(Image, fields=['image', 'main'], extra=6 - len(images))
    if request.method == 'POST':
        form = images_formset(request.POST or None, request.FILES or None)
        if form.is_valid():
            for obj in form:
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
            # return HttpResponseRedirect(reverse('property:index', ))
            return HttpResponseRedirect(reverse('property:detail', args=(prop.id,)))

    images_formset = images_formset(queryset=images)

    return render(request, 'properties/new_property.html', {'form': images_formset, 'propiedad': prop_id, 'page': 2})


def property_detail(request, prop_id):
    prop = get_object_or_404(Property, id=prop_id)
    form = ContactForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            name_in = form.cleaned_data['name']
            phone_in = form.cleaned_data['phone']
            message_in = form.cleaned_data['message']
            try:
                email_in = form.cleaned_data['email']
            except KeyError:
                print("no email provided")
                email_in = 'noemail@nomail.com'
            contact, _ = Contact.objects.get_or_create(propiedad=prop, name=name_in, phone=phone_in,
                                                       email=email_in, message=message_in)
            address = prop.address_col.get()
            address_parsed = urllib.parse.quote(str(address))
            print(address_parsed)
            # ******** email sending ********
            # //TODO: move email from property_detail to a funtion in tasks.py after setting up Celery
            file = "/media/{}".format(prop.gallery.get(main=True).image)
            data = {'propiedad': contact.propiedad, 'name': contact.name, 'phone': contact.phone,
                    'email': contact.email, 'message': contact.message, 'image': file, 'addr_parse': address_parsed}
            html_content = render_to_string('properties/contact_email.html', {'data': data})
            subject = '{} esta interesad@ en la propiedad: {} - {}'.format(data['name'].title(),
                                                                           data['propiedad'].title,
                                                                           data['propiedad'].code)
            msg = EmailMultiAlternatives(subject, html_content, prop.manager.email, prop.owner.email)
            msg.content_subtype = "html"
            msg.mixed_subtype = "related"
            img = open(file[1::], 'rb').read()
            url = file
            image = MIMEImage(img, 'jpg')
            image.add_header('Content-ID', '<{}>'.format(url))
            image.add_header("Content-Disposition", "inline", filename=url)
            msg.attach(image)

            try:
                msg.send()
                message = gettext('Your information has been sent to our agents! Thank you')
                print("email_sent")
                return render(request, 'properties/contact_form.html', {'mess': message, })
            except SMTPAuthenticationError:
                message = gettext('Something went wrong, please try again or contact agent by phone or whatsapp')
                return render(request, 'properties/contact_form.html', {'form': form, 'mess': message, })
            # ****************

        elif request.is_ajax():
            return render(request, 'properties/contact_form.html', {'form': form})
    try:
        address = prop.address_col.get()
        geo_data = get_coordinates(str(address))
    except ObjectDoesNotExist:
        geo_data = {'lat':  '4.624335', 'lng': '-74.063644'}
    visit = Visits(request)
    visit.add(prop_id)
    return render(request, 'properties/property-details.html',
                  {'prop': prop, 'form': form, 'lat': geo_data["lat"],
                   'lng': geo_data["lng"]})


def whatsapp_contact(request):
    prop_id = request.GET.get('id')
    prop = get_object_or_404(Property, id=prop_id)
    phone = prop.manager.profile.phone
    message = gettext("I am interested in the property: {}, Address: {}, code: {}. Is it still Available?") \
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

@login_required
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


def Template(request):  # view for debugging
    prop = Property.objects.last()
    a = prop.address_col.get()
    geo_data = get_coordinates(str(a))
    template = 'properties/maps.html'
    data = {'propiedad': prop, 'name': "nombre apellido", 'phone': "1234456809",
            'email': "email@email.com", 'geo_data': geo_data}
    return render(request, template, {'data': data})


def contact_us(request):
    form = ContactForm(request.POST or None, )
    if request.method == 'POST':
        if form.is_valid():
            name_in = form.cleaned_data['name']
            phone_in = form.cleaned_data['phone']
            mess_in = form.cleaned_data['message']
            try:
                email_in = form.cleaned_data['email']
            except KeyError:
                print("no email provided")
                email_in = 'noemail@nomail.com'
            # ******** email sending ********
            # //TODO: move email from contact_us to a funtion in tasks.py after setting up Celery
            # html_content = render_to_string('properties/contact_email.html', {'data': data})
            subject = 'MENSAJE DE {}'.format(name_in.title())
            message = "Nombre: {}, Email: {}, Phone: {}, Message: {}".format(name_in, email_in, phone_in, mess_in)
            send_mail(subject, message, 'camilo1rp@gmail.com', ['camilo1rp@gmail.com'])
            # ****************
    return render(request, 'properties/contact.html', {'form': form})


@login_required
def pause(request, prop_id):
    try:
        prop = Property.objects.get(id=prop_id)
    except ObjectDoesNotExist:
        return HttpResponse(gettext("Property does not exist"))
    if request.user not in [prop.manager, prop.owner]:
        return HttpResponse(gettext("Access denied, you don't own or manage this property"))
    print(prop.pause)
    if prop.pause:
        prop.pause = False
    else:
        prop.pause = True
    prop.save()
    print(prop.pause)
    # return JsonResponse({'a':1})
    # return render(request, 'account/dashboard.html')
    return HttpResponse(json.dumps(2), content_type='application/json')
