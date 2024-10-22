from django.urls import path
from .views import CreateEventView, EventSuccessView, submit_event, EventListView, EditEventView

#EventListView

urlpatterns = [
    path('create/', CreateEventView.as_view(), name='event_create'),
    path('list/', EventListView.as_view(), name='events_list'),
    path('create/success/', EventSuccessView.as_view(), name='event_success'), 
    path('create/submit_event/', submit_event ,name='submit_event' ),
    path('edit/<int:pk>/', EditEventView.as_view() ,name='edit_event'),
]

