# urls.py
from django.urls import path
from . import views

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import LocationViewSet, vista

router = DefaultRouter()
router.register(r'locations', LocationViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
]

