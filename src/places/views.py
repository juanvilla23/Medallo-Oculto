from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse
from django.contrib import messages
from cloudinary.uploader import upload
import requests
import os
from .models import InterestPlace
from .forms import PlaceForm

class CreatePlaceView(CreateView):
    model = InterestPlace
    template_name = 'Formulario_agregar_lugares.html'
    form_class = PlaceForm 

    def form_valid(self, form):   
        
        # Geocodificar la dirección
        API_KEY_GC = os.getenv('API_KEY_GC')
        address = form.cleaned_data.get('address')

        # URL y parámetros de la API de geocodificación
        base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
        params = {'address': address, 'key': API_KEY_GC}
        response = requests.get(base_url, params=params)

        if response.status_code == 200:
            data = response.json()
            if data['status'] == 'OK':
                location = data['results'][0]['geometry']['location']
                form.instance.latitude = location['lat']
                form.instance.longitude = location['lng']
            else:
                messages.error(self.request, 'No se encontró la dirección.')
                return redirect('create_place')
        else:
            messages.error(self.request, 'Error al conectarse con la API de geocodificación.')
            return redirect('create_place')

        # Manejar la subida de imágenes a Cloudinary
        images = self.request.FILES.getlist('images')
        image_urls = []
        for img in images:
            upload_response = upload(img)
            image_urls.append(upload_response['url'])

        # Guardar la instancia del lugar con las imágenes y coordenadas
        form.instance.images = image_urls
        form.instance.status = False  # O puedes configurar el status de otro modo

        return super().form_valid(form)


class PlaceListView(ListView):
    model = InterestPlace
    template_name = 'VisualizarPlaces.html'
    context_object_name = 'places'


class EditPlaceView(UpdateView):
    model = InterestPlace
    template_name = 'Formulario_agregar_lugares.html'
    form_class = PlaceForm

    def get_success_url(self):
        return reverse('places_list')


def submit_place(request):
    if request.method == 'POST':
        form = PlaceForm(request.POST, request.FILES)
        if form.is_valid():
            # Geocodificar la dirección antes de guardar
            API_KEY_GC = os.getenv('API_KEY_GC')
            address = form.cleaned_data.get('address')
            base_url = 'https://maps.googleapis.com/maps/api/geocode/json'
            params = {'address': address, 'key': API_KEY_GC}
            response = requests.get(base_url, params=params)

            if response.status_code == 200:
                data = response.json()
                if data['status'] == 'OK':
                    location = data['results'][0]['geometry']['location']
                    form.instance.latitude = location['lat']
                    form.instance.longitude = location['lng']
                else:
                    messages.error(request, 'No se encontró la dirección.')
                    return render(request, 'Formulario_agregar_lugares.html', {'form': form})
            else:
                messages.error(request, 'Error al conectarse con la API de geocodificación.')
                return render(request, 'Formulario_agregar_lugares.html', {'form': form})

            # Manejar la subida de imágenes a Cloudinary
            images = request.FILES.getlist('images')
            image_urls = []
            for img in images:
                upload_response = upload(img)
                image_urls.append(upload_response['url'])

            # Guardar la instancia del lugar con las imágenes
            lugar = form.save(commit=False)
            lugar.images = image_urls
            lugar.save()

            messages.success(request, 'Lugar creado exitosamente.')
            return redirect(reverse('interest_place_list'))  # Redirige a la lista de lugares
        else:
            # Muestra los errores de validación en el mensaje
            messages.error(request, f'Error al crear el lugar: {form.errors}')  
    else:
        form = PlaceForm()  # Inicializa el formulario vacío si no es POST

    return render(request, 'Formulario_agregar_lugares.html', {'form': form})
