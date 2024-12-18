"""
URL configuration for MedalloOculto project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from tests import views as testsView

from django.conf import settings
from django.conf.urls.static import static
from places import views as PlaceViews

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('routes.urls')),
    path('tests/', include('tests.urls')),
    path('routes/', include('routes.urls')),
    path('views/', include('views.urls')),
    path('Formulario/',PlaceViews.Mostrar_formulario,name='Mostrar_formulario'),
    path('add_place/',PlaceViews.add_place,name='add_place'),
    path('Visualizar/',PlaceViews.visualizarPlaces,name='visualizarPlaces'),
    path('users/',include('users.urls')),
    path('events/', include('events.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
