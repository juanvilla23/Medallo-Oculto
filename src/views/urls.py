from django.urls import path
from .views import (InterestPlaceListView, delete_interest_place, InterestPlaceUpdateView, 
                    InterestPlaceDetailView, RouteListView, delete_route, RouteUpdateView, RouteDetailView)

urlpatterns = [
    path('lugares/', InterestPlaceListView.as_view(), name='interest_place_list'),
    path('lugares/eliminar/<int:pk>/', delete_interest_place, name='interest_place_delete'),
    path('lugares/editar/<int:pk>/', InterestPlaceUpdateView.as_view(), name='interest_place_edit'),
    path('lugares/ver/<int:pk>/', InterestPlaceDetailView.as_view(), name='interest_place_view'),

    path('rutas/', RouteListView.as_view(), name='route_list'),  # Lista de rutas
    path('rutas/eliminar/<int:pk>/', delete_route, name='route_delete'),  # Eliminar ruta
    path('rutas/editar/<int:pk>/', RouteUpdateView.as_view(), name='route_edit'),  # Editar ruta
    path('rutas/ver/<int:pk>/', RouteDetailView.as_view(), name='route_view'),  # Ver detalles de ruta
]