from django.urls import path
from . import views

urlpatterns = [
    path('', views.main_route, name='main_route'),
]