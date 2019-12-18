from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Property, AddressCol


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'price_str', 'followers']


class AddressColForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update({'size': 4})

    class Meta:
        model = AddressCol
        exclude = []


class ImageForm(forms.Form):
    property_id = forms.CharField(max_length=12)
    image = forms.ImageField()






