from datetime import datetime
from django.contrib.auth.models import User
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, ListView, UpdateView
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import EventForm
from django.shortcuts import get_object_or_404
from .models import Event, EventImage
from cloudinary.uploader import upload
from django.utils import timezone  # Si prefieres manejar zonas horarias locales/globales


class CreateEventView(CreateView):
    model = Event
    template_name = 'events/event-create.html'
    fields = ['name', 'description', 'price', 'date_and_time', 'categories', 'capacity']

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



def submit_event(request, event_id=None):
    event = get_object_or_404(Event, id=event_id) if event_id else None

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            date_time_str = request.POST.get('date_and_time')  
            try:
                # Convierte la cadena de fecha y hora al objeto datetime
                event.date_and_time = datetime.strptime(date_time_str, '%d/%m/%Y %I:%M %p')
            except:
                pass

            event.promotor = request.user
            event.save()

            # Subir y guardar cada imagen
            for image in request.FILES.getlist('images'):
                uploaded_image = upload(image)
                EventImage.objects.create(event=event, image=uploaded_image['secure_url'])

            messages.success(request, 'Evento guardado correctamente.')
            return redirect(reverse('event_success'))
    else:
        form = EventForm(instance=event)

    return render(request, 'events/event-create.html', {'form': form, 'event': event})

