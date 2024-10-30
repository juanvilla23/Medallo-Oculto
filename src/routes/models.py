from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.contrib.auth.models import User
from places.models import InterestPlace



class InterestPlace(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    categories = ArrayField(models.CharField(max_length=200), blank=True, null=True)
    #categories= models.CharField(max_length=200,null=True)
    #rating = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.BooleanField(default=True)
    latitude = models.DecimalField(max_digits=9, decimal_places=6)
    longitude = models.DecimalField(max_digits=9, decimal_places=6)
    images = ArrayField(models.CharField(max_length=600), blank=True, null=True)
    address=models.CharField(max_length=200,default="Dirección desconocida")
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    

    class Meta:
        db_table = 'interest_place'

    def __str__(self):
        return self.name
    
    @property
    def first_image(self):                       #En el campo de images hay una lista con links de imagenes, 
        if self.images and len(self.images) > 0: # esta funciión  retorna el primer link de esa lista 
            return self.images[0]
        return None
    @property
    def listar_categorias(self):
        lista="Categories: "
        max=len(self.categories)-1
        for  i in range(len(self.categories)):
            if i!=max:
                lista=lista+self.categories[i]+", "
            else:
                lista=lista+self.categories[i]
        return lista            
            
            

class Route(models.Model):
    #creator = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    creator = models.ForeignKey(User, on_delete=models.CASCADE,default=1)
    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1000, blank=True, null=True)
    places = models.ManyToManyField(InterestPlace, blank=True)
    #events = models.ManyToManyField(Event, blank=True)  
    #rating = models.DecimalField(max_digits=3, decimal_places=2)

    class Meta:
        db_table = 'route'

    def __str__(self):
        return self.name

class RouteInterestPlace(models.Model):
    route = models.ForeignKey(Route, on_delete=models.CASCADE, related_name="route_places")
    place = models.ForeignKey(InterestPlace, on_delete=models.CASCADE, related_name="place_routes")
    order = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'route_interest_place'  # Especifica el nombre exacto de la tabla
        unique_together = ('route', 'place')

    def __str__(self):
        return f"{self.route.name} - {self.interest_place.name}"
