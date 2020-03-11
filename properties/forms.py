from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from .models import Property, AddressCol, Image, Contact, BusinessType
import string

PREFIJOS = [tuple([x, x]) for x in string.ascii_uppercase[:8]]
[PREFIJOS.append(tuple(['{} BIS'.format(x), '{} BIS'.format(x)])) for x in string.ascii_uppercase[:8]]
[PREFIJOS.append(tuple(['{} SUR'.format(x), '{} SUR'.format(x)])) for x in string.ascii_uppercase[:8]]
PREFIJOS.insert(0, tuple(['', '']))

VIAS = [
    ('CL', 'Calle'),
    ('CR', _('Carrera')),
    ('TV', _('Transversal')),
    ('DG', _('Diagonal')),
    ('AV', _('Avenida')),
    ('AC', _('Avenida calle')),
    ('AK', _('Avenida carrera')),
]


class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='6', cols='85')
        self.fields['description'].widget.attrs['placeholder'] = \
            gettext("Add extra information that adds value to your property. i.e. common areas, services, security, "
                    "location, etc.")
        self.fields['owner'].empty_label = _('select owner')
        self.fields['price_str'].label = _('price')

    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'active', 'followers', 'manager', 'upload_code', 'promoted', 'pause',
                   'is_project', 'area_pro', 'sale', 'sold', 'facilities', 'rooms_max', 'baths_max', 'parking_max',
                   'area_max']


class PropertyForm2(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='6', cols='85')
        self.fields['description'].widget.attrs['placeholder'] = \
            gettext("Add extra information that adds value to your property. i.e. common areas, services, security, "
                    "location, etc.")
        self.fields['owner'].empty_label = _('select owner')
        self.fields['price_str'].label = _('Price: from')
        self.fields['rooms'].label = _('Rooms: from')
        self.fields['rooms_max'].label = _('Rooms: up to')
        self.fields['baths'].label = _('Baths: from')
        self.fields['baths_max'].label = _('Baths: up to')
        self.fields['sale'].label = _('# For sale')
        self.fields['sold'].label = _('# Sold')
        self.fields['area_built'].label = _('Area: from')
        self.fields['area_max'].label = _('Area: to')
        self.fields['parking'].label = _('Parking: from')
        self.fields['parking_max'].label = _('Parking: to')

    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'active', 'followers', 'manager', 'upload_code', 'promoted', 'pause',
                   'area_total']


class AddressColForm(forms.ModelForm):
    prefijo_via = forms.CharField(widget=forms.Select(choices=PREFIJOS), required=False)
    prefijo_numero = forms.CharField(widget=forms.Select(choices=PREFIJOS), required=False)
    tipo_via = forms.CharField(widget=forms.Select(choices=VIAS), required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_via'].widget.attrs.update(placeholder='ej. Calle')
        self.fields['via'].widget.attrs.update(placeholder='ej. 10')
        # self.fields['prefijo_via'].widget.attrs.update(empty_label='ej. A',)
        self.fields['numero'].widget.attrs.update(placeholder='ej. 11')
        self.fields['prefijo_numero'].widget.attrs.update(placeholder='ej. BIS')
        self.fields['placa'].widget.attrs.update(placeholder='ej. 12')
        self.fields['ciudad'].widget.attrs.update(placeholder='ej. Bogota')
        self.fields['departamento'].widget.attrs.update(placeholder='ej. Cundinamarca')
        self.fields['departamento'].empty_label = "Departamento"  
        self.fields['ciudad'].empty_label = "Ciudad"  
        self.fields['barrio'].widget.attrs.update(placeholder='ej. Cedritos', required=False)
        self.fields['prefijo_via'].label = 'prefijo'
        self.fields['prefijo_numero'].label = 'prefijo'

    class Meta:
        model = AddressCol
        exclude = []


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        exclude = ['propiedad']



class ContactForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['message'].widget.attrs.update(rows='4', cols='25')

    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email', 'message']


class MultiPropForm(forms.Form):
    csv_file = forms.FileField(label=_('csv file'))
    owner = forms.ModelChoiceField(queryset=User.objects.all())


