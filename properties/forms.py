from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.utils.translation import gettext
from .models import Property, AddressCol, Image, Contact, BusinessType, Project
from .validators import TIPO_PRO, TIPO_BUS, STATUS_PRO
import string

PREFIJOS = [tuple([x, x]) for x in string.ascii_uppercase[:8]]
[PREFIJOS.append(tuple(['{} BIS'.format(x), '{} BIS'.format(x)])) for x in string.ascii_uppercase[:8]]
PREFIJOS.append(tuple(['SUR', 'SUR']))
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


class ProjectForm(forms.ModelForm):
    """Form for new project"""
    properties = forms.ModelMultipleChoiceField(queryset=Property.objects.all())
    photo2 = forms.ImageField()
    photo3 = forms.ImageField()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)

    class Meta:
        model = Project
        exclude = ['name_slug', 'manager']


class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        manager = kwargs.pop('manager')
        super().__init__(*args, **kwargs)

        self.fields['project'] = forms.ModelChoiceField(Project.objects.filter(manager=manager))
        self.fields['project'].required = False
        self.fields['description'].widget.attrs.update(rows='6', cols='85')
        self.fields['description'].widget.attrs['placeholder'] = \
            gettext("Add extra information that adds value to your property."
                    " i.e. common areas, services, security, location, etc.")
        self.fields['owner'].empty_label = _('select owner')
        # self.fields['owner'].widget.attrs['disabled'] = True
        self.fields['price_str'].label = _('price')

    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'active', 'followers', 'manager', 'upload_code', 'promoted', 'pause']


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


# *********New style forms***********"""


class SearchBarForm(forms.Form):
    """Index main search bar form inputs"""
    business_type = forms.ChoiceField(choices=TIPO_BUS)
    property_type = forms.ChoiceField(choices=TIPO_PRO)
    property_condition = forms.ChoiceField(choices=STATUS_PRO)
    city = forms.CharField(max_length=127, required=False)
    state = forms.CharField(max_length=127, required=False)
    locality = forms.CharField(max_length=127, required=False)
