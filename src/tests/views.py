# views.py
from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import Location
from .serializers import LocationSerializer

class LocationViewSet(viewsets.ModelViewSet):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer

def vista(request):
    return render(request, 'vista.html')
