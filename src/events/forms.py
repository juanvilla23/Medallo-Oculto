from django import forms
from events.models import Event

class EventForm(forms.ModelForm):
    #images = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}), required=False)

    class Meta:
        model = Event
        fields = ['name', 'description', 'price', 'date_and_time', 'categories', 'capacity', 'address']
        widgets = {
            'date_and_time': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }
