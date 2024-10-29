from django.db import models
from django.contrib.auth.models import User

class Promotor(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo =models.CharField(max_length=100,default="Promotor")
    telefono = models.CharField(max_length=100)
    
    # Agrega más campos específicos para Promotor

    def __str__(self):
        return f"Promotor: {self.user.username}"

# Modelo para Turista
class Turista(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    tipo =models.CharField(max_length=100,default="Turista")
    # Agrega más campos específicos para Turista

    def __str__(self):
        return f"Turista: {self.user.username}"

# Create your models here.