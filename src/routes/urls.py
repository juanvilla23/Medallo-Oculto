from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_route, name='main_route'),
    path('get-markers/', views.get_markers, name='get_markers'),
    path('search/', views.search, name='search'),
]