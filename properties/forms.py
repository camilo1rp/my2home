from django import forms
from django.forms import Textarea
from django.utils.translation import gettext_lazy as _
from .models import Property, AddressCol


class PropertyForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(rows='2', cols='40')
        self.fields['owner'].empty_label = _('select owner')
        self.fields['manager'].empty_label = _('select manager')


    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'price_str', 'followers']


class AddressColForm(forms.ModelForm):
    class Meta:
        model = AddressCol
        exclude = []


class ImageForm(forms.Form):
    property_id = forms.CharField(max_length=12)
    image = forms.ImageField()






