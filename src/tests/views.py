# views.py
import folium
from django.shortcuts import render

def map_view(request):
    # Crear un mapa de Folium
    m = folium.Map(location=[45.5236, -122.6750], zoom_start=13)

    # Generar el HTML del mapa
    map_html = m._repr_html_()

    # Coordenadas de ejemplo para los marcadores
    markers = [
        {"lat": 45.5236, "lng": -122.6750, "popup": "Portland, OR"},
        {"lat": 45.528, "lng": -122.680, "popup": "Another Place"}
    ]

    # Pasar el HTML del mapa y las coordenadas de los marcadores a la plantilla
    context = {'map_html': map_html, 'markers': markers}
    return render(request, './map_template.html', context)

