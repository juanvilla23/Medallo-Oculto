from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.views.generic import CreateView, ListView, UpdateView
from django.urls import reverse
from django.contrib import messages
from cloudinary.uploader import upload
import requests
import os
from .models import InterestPlace
from .forms import PlaceForm  # Asumiendo que tienes un formulario PlaceForm

class CreatePlaceView(CreateView):
    model = InterestPlace
    template_name = 'Formulario_agregar_lugares.html'
    form_class = PlaceForm 
"""
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
            print(f"Error en la solicitud: {data['status']}")
            messages.error(request, 'NO SE ENCONTRÓ LA DIRECCIÓN.')
            return redirect("/Formulario")
    
    image_urls = []
    images = request.FILES.getlist('images')  # Obtener múltiples archivos
    for img in images:
        upload_response = upload(img)  # Subir la imagen a Cloudinary
        image_urls.append(upload_response['url'])  # Obtener la URL de la imagen
            
    
   
    
    place=InterestPlace.objects.create(name=nameF, description=descriptionF,categories=categoriaF,
                                       status=False, latitude=latitudF,longitude=longitudF,images=image_urls,address=addressF)
    return redirect("/Visualizar")

def visualizarPlaces(request):
    places=InterestPlace.objects.all()   
    return render(request, 'VisualizarPlaces.html',{'places':places})
    
    
    
    

    
