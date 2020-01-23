from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Property, AddressCol, Image, Contact, BusinessType
import string

CHOICES = [tuple([x, x]) for x in string.ascii_uppercase[:10]]
[CHOICES.append(tuple(['{} BIS'.format(x),'{} BIS'.format(x)])) for x in string.ascii_uppercase[:10]]
CHOICES.insert(0, tuple(['', '']))


class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='4', cols='40')
        self.fields['owner'].empty_label = _('select owner')
        self.fields['price_str'].label = _('price')

    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'active', 'followers', 'manager', 'upload_code']


class AddressColForm(forms.ModelForm):
    prefijo_via = forms.CharField(widget=forms.Select(choices=CHOICES), required=False)
    prefijo_numero = forms.CharField(widget=forms.Select(choices=CHOICES), required=False)

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
        exclude = []


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['name', 'phone', 'email']


class MultiPropForm(forms.Form):
    csv_file = forms.FileField(label=_('csv file'))
    owner = forms.ModelChoiceField(queryset=User.objects.all())


