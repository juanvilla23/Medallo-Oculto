from django import forms
from .models import Route

class RouteForm(forms.ModelForm):
    
    class Meta:
        model = Route
        fields = ['name', 'description', 'places']  # Añadir 'rating' si también se va a capturar en el formulario.
