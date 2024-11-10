from django.urls import path
from .views import (InterestPlaceListView, delete_interest_place, InterestPlaceUpdateView, 
                    InterestPlaceDetailView, RouteListView, delete_route, RouteUpdateView, RouteDetailView, remove_image, add_route, add_route_interest_places)

urlpatterns = [
    path('lugares/', InterestPlaceListView.as_view(), name='interest_place_list'),
    path('lugares/eliminar/<int:pk>/', delete_interest_place, name='interest_place_delete'),
    path('lugares/editar/<int:pk>/', InterestPlaceUpdateView.as_view(), name='interest_place_edit'),
    path('lugares/ver/<int:pk>/', InterestPlaceDetailView.as_view(), name='interest_place_view'),

    path('rutas/crear/', add_route, name='add_route'),
    path('rutas/<int:route_id>/lugares/', add_route_interest_places, name='add_route_interest_places'),

    path('rutas/', RouteListView.as_view(), name='route_list'),  # Lista de rutas
    path('rutas/eliminar/<int:pk>/', delete_route, name='route_delete'),  # Eliminar ruta
    path('rutas/editar/<int:pk>/', RouteUpdateView.as_view(), name='route_edit'),  # Editar ruta
    path('rutas/ver/<int:pk>/', RouteDetailView.as_view(), name='route_view'),  # Ver detalles de ruta

    path('views/lugares/<int:pk>/eliminar_imagen/<path:public_id>/', remove_image, name='remove_image'),

]