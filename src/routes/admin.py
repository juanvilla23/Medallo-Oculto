from django.contrib import admin
from .models import (Route, InterestPlace, RouteInterestPlace)

admin.site.register(Route)
admin.site.register(InterestPlace)
admin.site.register(RouteInterestPlace)