from django import forms
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from .models import Property, AddressCol


class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='2', cols='40')
        self.fields['owner'].empty_label = _('select owner')

    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'followers', 'manager']


class AddressColForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['tipo_via'].widget.attrs.update(placeholder='ej. Calle')
        self.fields['via'].widget.attrs.update(placeholder='ej. 10')
        self.fields['prefijo_via'].widget.attrs.update(placeholder='ej. A')
        self.fields['numero'].widget.attrs.update(placeholder='ej. 11')
        self.fields['prefijo_numero'].widget.attrs.update(placeholder='ej. BIS')
        self.fields['placa'].widget.attrs.update(placeholder='ej. 12')
        self.fields['ciudad'].widget.attrs.update(placeholder='ej. Bogota')
        self.fields['departamento'].widget.attrs.update(placeholder='ej. Cundinamarca')
        self.fields['barrio'].widget.attrs.update(placeholder='ej. Cedritos')
        self.fields['prefijo_via'].label = 'prefijo'
        self.fields['prefijo_numero'].label = 'prefijo'

    class Meta:
        model = AddressCol
        exclude = []

class ImageForm(forms.Form):
    property_id = forms.CharField(max_length=12)
    image = forms.ImageField()






