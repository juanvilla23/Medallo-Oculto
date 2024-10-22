from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['name', 'description', 'images', 'price', 'date_and_time', 'categories', 'capacity', 'address']
        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }