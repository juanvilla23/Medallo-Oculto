from django.shortcuts import render
from django.db.models import Q
from django.http import JsonResponse
from .models import (InterestPlace, Route, RouteInterestPlace)
from django.db import connection
from django.db.models.functions import Lower
import re

# Create your views here.
def main_route(request):
    return render(request, 'main_route.html')

def get_markers(request):
    # Obtén todos los lugares de interés de la base de datos
    interest_places = InterestPlace.objects.all().filter(status=True)

    # Serializa los datos que quieres enviar en el JSON
    markers = list(interest_places.values('id', 'name', 'description', 'latitude', 'longitude', 'images', 'categories'))

    # Devuelve la respuesta en formato JSON
    return JsonResponse({'markers': markers})

def is_safe_query(query):
    # Expresión regular que verifica si la cadena contiene solo letras y números
    pattern = re.compile(r'^[a-zA-Z0-9]+$')
    
    if pattern.match(query):
        return True
    return False

def search(request):
    query = request.GET.get('q', '')
    query2 = request.GET.get('i', '')

    if query and query2:
        # Convertimos la consulta a minúsculas y aplicamos unaccent usando SQL sin procesar.
        normalized_query = query.lower()

        if not is_safe_query(query):
            return JsonResponse({'error': 'Invalid characters in query. Only letters and numbers are allowed.'}, status=400)

        if query2 == 'route':
            # Utilizamos SQL sin procesar para aplicar unaccent en el campo 'name'
            routes = Route.objects.raw('''
                SELECT * FROM route
                WHERE unaccent(lower(name)) LIKE unaccent(lower(%s))
                LIMIT 5
            ''', [f'%{normalized_query}%'])
            results = [{'name': route.name, 'id': route.id} for route in routes]

        elif query2 == 'place':
            # Utilizamos SQL sin procesar para aplicar unaccent en 'name' y 'description'
            interest_places = InterestPlace.objects.raw('''
                SELECT * FROM interest_place
                WHERE unaccent(lower(name)) LIKE unaccent(lower(%s))
                OR unaccent(lower(description)) LIKE unaccent(lower(%s))
                LIMIT 5
            ''', [f'%{normalized_query}%', f'%{normalized_query}%'])
            results = [{'name': place.name, 'description': place.description, 'id': place.id} for place in interest_places]

        elif query2 == 'event':
            return JsonResponse({'error': 'No query provided'}, status=400)

        else:
            return JsonResponse({'error': 'No query provided'}, status=400)

        return JsonResponse(results, safe=False)

    return JsonResponse({'error': 'No query provided'}, status=400)