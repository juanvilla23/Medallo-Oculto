from django.db import models
from django.contrib.postgres.fields import ArrayField

class InterestPlace(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    categories = ArrayField(models.CharField(max_length=100), blank=True, null=True)
    #rating = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    images = ArrayField(models.CharField(max_length=600), blank=True, null=True)

    class Meta:
        db_table = 'interest_place'

    def __str__(self):
        return self.name

class Route(models.Model):
    #creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    #rating = models.DecimalField(max_digits=3, decimal_places=2)
    #comments = models.TextField()

    class Meta:
        db_table = 'route'

    def __str__(self):
        return self.name

class RouteInterestPlace(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE)
    interest_place = models.ForeignKey(InterestPlace, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'route_interest_place'  # Especifica el nombre exacto de la tabla
        unique_together = ('route', 'interest_place')

    def __str__(self):
        return f"{self.route.name} - {self.interest_place.name}"
