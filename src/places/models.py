from django.db import models
from django.contrib.postgres.fields import ArrayField
from multiselectfield import MultiSelectField


class InterestPlace(models.Model):

    """CATEGORY_CHOICES = [
        ('culture', 'Culture'),
        ('Film', 'Movies and cinema'),
        ('Art', 'Art'),
        ('Technology', 'Technology'),
        ('Business', 'Business'),
     ]
    """

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
        lista=""
        max=len(self.categories)-1
        for  i in range(len(self.categories)):
            if i!=max:
                lista=lista+self.categories[i]+", "
            else:
                lista=lista+self.categories[i]
        return lista            