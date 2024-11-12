from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from multiselectfield import MultiSelectField
from cloudinary.models import CloudinaryField

class Event(models.Model):
    STATUS_OPTIONS = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]

    CATEGORY_CHOICES = [
        ('Music', 'Music'),
        ('Film', 'Film'),
        ('Art', 'Art'),
        ('Technology', 'Technology'),
        ('Business', 'Business'),
     ]

    name = models.CharField(max_length=200)
    description = models.TextField(max_length=1500)
    price = models.PositiveIntegerField(null=True, blank=True)
    date_and_time = models.DateTimeField()
    categories = MultiSelectField(choices=CATEGORY_CHOICES, max_choices=3, max_length=200)
    status = models.CharField(max_length=10, choices=STATUS_OPTIONS, default='pending')
    capacity = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    interested_people = models.ManyToManyField(User, related_name='interested_events', blank=True)
    longitude = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    address = models.CharField(max_length=200)

    def __str__(self):
        return self.name

    @property
    def first_image(self):
        first_image = self.images.first()  # Utiliza `self.images` para acceder al conjunto relacionado de `EventImage`
        return first_image.image.url if first_image else None

class EventImage(models.Model):
    event = models.ForeignKey(Event, related_name='images', on_delete=models.CASCADE)
    image = CloudinaryField('image')

