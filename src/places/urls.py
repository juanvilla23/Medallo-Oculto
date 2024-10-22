from django.urls import path
from .views import CreatePlaceView, submit_place, PlaceListView, EditPlaceView

#PlaceListView

urlpatterns = [
    path('create/', CreatePlaceView.as_view(), name='place_create'),
    path('list/', PlaceListView.as_view(), name='places_list'),
    #path('create/success/', PlaceSuccessView.as_view(), name='place_success'), 
    path('create/submit_place/', submit_place , name='submit_place' ),
    path('edit/<int:pk>/', EditPlaceView.as_view() ,name='edit_place'),
]
