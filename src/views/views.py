from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DetailView
from routes.models import  Route, RouteInterestPlace
from places.models import InterestPlace
from django.urls import reverse_lazy
from django.core.paginator import Paginator

# Vista para listar los lugares de interés con paginación
class InterestPlaceListView(ListView):
    model = InterestPlace
    template_name = 'interest_places.html'  # Tu plantilla
    context_object_name = 'places'    # Nombre de la variable para pasar a la plantilla
    paginate_by = 10                           # Número de elementos por página

# Vista para eliminar un lugar de interés
def delete_interest_place(request, pk):
    place = get_object_or_404(InterestPlace, pk=pk)
    place.delete()
    return redirect('interest_place_list')

# Vista para editar un lugar de interés
class InterestPlaceUpdateView(UpdateView):
    model = InterestPlace
    fields = ['name', 'description', 'categories', 'latitude', 'longitude', 'images', 'address']
    template_name = 'interestplace_form.html'
    success_url = reverse_lazy('interest_place_list')

# Vista para ver un lugar de interés
class InterestPlaceDetailView(DetailView):
    model = InterestPlace
    template_name = 'interestplace_detail.html'




class RouteDetailView(DetailView):
    model = Route
    template_name = 'route_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Obtener los lugares de interés relacionados con la ruta
        context['places'] = RouteInterestPlace.objects.filter(route=self.object)
        return context

# Vista para listar las rutas con paginación
class RouteListView(ListView):
    model = Route
    template_name = 'routes.html'  # Plantilla que se renderizará
    context_object_name = 'routes'  # Nombre de la variable en la plantilla
    paginate_by = 10  # Número de rutas por página


def delete_route(request, pk):
    route = get_object_or_404(Route, pk=pk)
    route.delete()
    return redirect('route_list')  # Redirige a la lista de rutas después de eliminar

class RouteUpdateView(UpdateView):
    model = Route
    fields = ['name']  # Campos que se pueden editar
    template_name = 'route_form.html'  # Plantilla del formulario de edición
    success_url = reverse_lazy('route_list')  # Redirige a la lista de rutas después de editar

