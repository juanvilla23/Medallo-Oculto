from django.shortcuts import render,redirect
from django.http import HttpResponse 
from routes.models import InterestPlace
from cloudinary.uploader import upload
import requests 
from django.contrib import messages
import os
import json

from django.http import JsonResponse

def Mostrar_formulario(request):
    return render(request,'Formulario_agregar_lugares.html')
def add_place(request):
    
    nameF=request.POST['place_name']
    descriptionF=request.POST['place_description']
    categoriaF=request.POST.getlist('categoria_place')
    
    API_KEY_GC = os.getenv('API_KEY_GC')

    # La dirección que deseas geocodificar
    addressF =  request.POST['place_address'] #'Cra. 40 #51-24' #Pablo tobón uribe


    base_url = 'https://maps.googleapis.com/maps/api/geocode/json'

    # Parámetros de la solicitud
    params = {
        'address': addressF,
        'key': API_KEY_GC
    }

    # Realizar la solicitud GET a la API
    response = requests.get(base_url, params=params)

    # Verificar el código de estado de la respuesta
    if response.status_code == 200:
        # Convertir la respuesta a JSON
        data = response.json()
    # Verificar si la solicitud fue exitosa
        if data['status'] == 'OK':
            # Extraer las coordenadas (latitud y longitud)
            location = data['results'][0]['geometry']['location']
            print(f"Dirección: {addressF}")
            print(f"Latitud: {location['lat']}, Longitud: {location['lng']}")
            latitudF=location['lat']
            longitudF=location['lng']
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
    
    
    
    

    
