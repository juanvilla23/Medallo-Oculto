# forms.py en la aplicación `routes`
from django import forms
from .models import Route, RouteInterestPlace
from places.models import InterestPlace

class RouteForm(forms.ModelForm):
    places = forms.ModelMultipleChoiceField(
        queryset=InterestPlace.objects.all(),
        widget=forms.SelectMultiple(attrs={'size': 10}),  # Ajuste de visualización
        required=True,
        label="Select up to 20 Places",
        help_text="Use Ctrl (Cmd en Mac) para seleccionar múltiples lugares.",
    )

    class Meta:
        model = Route
        fields = ['name', 'description', 'places']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3}),
        }

    def clean_places(self):
        places = self.cleaned_data.get('places')
        if places and len(places) > 20:
            raise forms.ValidationError("You can select up to 20 places.")
        return places

    def save(self, *args, **kwargs):
        # Guarda el Route primero
        route = super().save(*args, **kwargs)
        
        # Aquí puedes establecer el valor de `order`
        order = 0  # Inicia con el primer valor para el orden

        for place in self.cleaned_data['places']:
            RouteInterestPlace.objects.create(route=route, places=places, order=order)
            order += 1  # Incrementa el valor para el próximo lugar

        return route

