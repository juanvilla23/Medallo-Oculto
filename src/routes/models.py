from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from places.models import InterestPlace


class Route(models.Model):
    #creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    places = models.ManyToManyField(InterestPlace, through='RouteInterestPlace', related_name='routes', blank=True)
    #rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'route'

    def __str__(self):
        return self.name

class RouteInterestPlace(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_places")
    place = models.ForeignKey(InterestPlace, on_delete=models.CASCADE, related_name="place_routes")
    order = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'route_interest_place'  # Especifica el nombre exacto de la tabla
        unique_together = ('route', 'place')

    def __str__(self):
        return f"{self.route.name} - {self.interest_place.name}"
