from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm
from .models import Event


class CreateEventView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    fields = ['name', 'description', 'images', 'price', 'date_and_time', 'categories', 'capacity']

    def form_valid(self, form):
        form.instance.promotor = self.request.user  # Asigna automáticamente el usuario actual como promotor del evento
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_success')

class EventSuccessView(TemplateView):
    template_name = 'events/event_success.html'

class EventListView (ListView):
    model=Event
    template_name='event_list.html'
    context_object_name= 'events'

class EditEventView(UpdateView):
    model = Event
    template_name = 'events/event-create.html'
    form_class = EventForm

    def form_valid(self, form):
        form.instance.promotor = self.request.user  # Asigna el promotor como el usuario actual
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_success')

from django.shortcuts import get_object_or_404

def submit_event(request, event_id=None):
    # Si existe un ID de evento, estamos editando
    if event_id:
        event = get_object_or_404(Event, id=event_id)  # Busca el evento o devuelve 404 si no existe
    else:
        event = None  # Si no hay ID, significa que es un evento nuevo

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)  # Pasa el evento existente si estamos editando
        if form.is_valid():
            event = form.save(commit=False)
            date_time_str = request.POST.get('date_and_time')
            try:
                event.date_and_time = datetime.strptime(date_time_str, '%d/%m/%Y %I:%M %p')
            except:
                pass

            event.promotor = User.objects.get(id=1)  # Asegúrate de ajustar esto según tu lógica de promotor
            event.save()
            
            if event_id:
                messages.success(request, 'El evento se ha actualizado correctamente.')
            else:
                messages.success(request, 'El evento se ha creado correctamente.')

            return redirect(reverse('event_success'))
        else:
            if event_id:
                messages.error(request, 'Hubo un error al actualizar el evento.')
            else:
                messages.error(request, 'Hubo un error al crear el evento.')
    else:
        form = EventForm(instance=event)  # Prellena el formulario con los datos del evento si existe

    return render(request, 'events/event-create.html', {'form': form, 'event': event})

