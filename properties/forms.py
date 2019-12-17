from django import forms
from django.utils.translation import gettext_lazy as _
from .models import Property, AddressCol


class PropertyForm(forms.ModelForm):
    class Meta:
        model = Property
        exclude = ['title_slug', 'code', 'seen', 'price_str', 'followers']


class AddressColForm(forms.ModelForm):

    class Meta:
        model = AddressCol
        exclude = []


