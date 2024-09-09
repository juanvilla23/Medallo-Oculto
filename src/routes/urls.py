from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_route, name='main_route'),
    path('get-markers/', views.get_markers, name='get_markers'),
    path('search/', views.search, name='search'),
    path('get_coords_by_id/', views.get_coords_by_id, name='get_coords_by_id'),
    path('get_route_coords_by_id/', views.get_route_coords_by_id, name='get_route_coords_by_id')
]