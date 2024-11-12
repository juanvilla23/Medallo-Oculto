from django.shortcuts import render

# Create your views here.
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
    template_name = 'event-create.html'
    fields = ['name', 'description', 'price', 'date_and_time', 'categories', 'capacity']

    def form_valid(self, form):
        form.instance.promotor = self.request.user  # Asigna automáticamente el usuario actual como promotor del evento
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_success')

class EventSuccessView(TemplateView):
    template_name = 'event_success.html'

class EventListView(ListView):
    model = Event
    template_name = 'event_list.html'
    context_object_name = 'events'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Establece `es_creador` en True si el usuario es el creador de al menos uno de los eventos
        context['es_creador'] = Event.objects.filter(creator=self.request.user).exists()
        return context


class EditEventView(UpdateView):
    model = Event
    template_name = 'event-create.html'
    form_class = EventForm

    def form_valid(self, form):
        form.instance.promotor = self.request.user  # Asigna el promotor como el usuario actual
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('event_success')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Verifica si el usuario actual es el creador del evento
        context['es_creador'] = self.request.user == self.get_object().creator
        return context





from django.http import HttpResponseForbidden

def submit_event(request, event_id=None):
    # Si estamos editando un evento, intenta obtenerlo de la base de datos
    event = get_object_or_404(Event, id=event_id) if event_id else None

    # Verifica si el usuario actual es el creador del evento cuando el evento ya existe
    es_creador = request.user == event.creator if event else True  # Nuevo evento implica que el usuario será el creador

    # Si el usuario no es el creador del evento, deniega el acceso
    if event and not es_creador:
        return HttpResponseForbidden("No tienes permiso para editar este evento.")

    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            event = form.save(commit=False)
            
            # Convierte la cadena de fecha y hora al objeto datetime
            date_time_str = request.POST.get('date_and_time')  
            try:
                event.date_and_time = datetime.strptime(date_time_str, '%d/%m/%Y %I:%M %p')
            except ValueError:
                pass  # Manejar error de fecha y hora si es necesario

            # Asigna el creador del evento al usuario actual
            event.creator = request.user
            event.save()

            # Subir y guardar cada imagen
            for image in request.FILES.getlist('images'):
                uploaded_image = upload(image)
                EventImage.objects.create(event=event, image=uploaded_image['secure_url'])
            print("se guardo el evento")

            messages.success(request, 'Evento guardado correctamente.')
            events2 = Event.objects.filter(creator=request.user)



            print(f"Valor {es_creador}")
            print(f"Cantidad {len(events2)}")
            return render(request, 'event_list.html', {'form': form, 'events2':events2})
    else:
        form = EventForm(instance=event)

    # Renderiza el formulario de creación/edición del evento
    return render(request, 'event-create.html', {'form': form,  'es_creador': es_creador})

