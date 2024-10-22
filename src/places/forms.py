from django import forms
from .models import InterestPlace

class PlaceForm(forms.ModelForm):
    class Meta:
        model = InterestPlace
        fields = ['name', 'description', 'categories', 'images','address']
        