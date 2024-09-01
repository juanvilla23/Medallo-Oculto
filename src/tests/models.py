from django.db import models

class Location(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    category = models.CharField(max_length=50)  # Para el filtrado dinámico

    def __str__(self):
        return self.name

