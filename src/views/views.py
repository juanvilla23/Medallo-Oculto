from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, UpdateView, DetailView
from routes.models import InterestPlace, Route, RouteInterestPlace
from django.urls import reverse_lazy
from django.core.paginator import Paginator

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from cloudinary.uploader import destroy  # Si usas Cloudinary para eliminar
from urllib.parse import unquote
import urllib.parse
from django.contrib import messages
from cloudinary.uploader import upload
from django.urls import reverse
from django.forms import ModelForm, ModelMultipleChoiceField
from django import forms
from django.views.generic.edit import View



# # Vista para listar los lugares de interés con paginación
# class InterestPlaceListView(ListView):
#     model = InterestPlace
#     template_name = 'interest_places.html'  # Tu plantilla
#     context_object_name = 'interest_places'    # Nombre de la variable para pasar a la plantilla
#     paginate_by = 10                           # Número de elementos por página

# # Vista para eliminar un lugar de interés
# def delete_interest_place(request, pk):
#     place = get_object_or_404(InterestPlace, pk=pk)
#     place.delete()
#     return redirect('interest_place_list')

# # Vista para editar un lugar de interés
# class InterestPlaceUpdateView(UpdateView):
#     model = InterestPlace
#     fields = ['name', 'description', 'categories', 'latitude', 'longitude', 'images', 'address']
#     template_name = 'interestplace_form.html'
#     success_url = reverse_lazy('interest_place_list')

# # Vista para ver un lugar de interés
# class InterestPlaceDetailView(DetailView):
#     model = InterestPlace
#     template_name = 'interestplace_detail.html'




# class RouteDetailView(DetailView):
#     model = Route
#     template_name = 'route_detail.html'

#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         # Obtener los lugares de interés relacionados con la ruta
#         context['interest_places'] = RouteInterestPlace.objects.filter(route=self.object)
#         return context

# # Vista para listar las rutas con paginación
# class RouteListView(ListView):
#     model = Route
#     template_name = 'routes.html'  # Plantilla que se renderizará
#     context_object_name = 'routes'  # Nombre de la variable en la plantilla
#     paginate_by = 10  # Número de rutas por página


# def delete_route(request, pk):
#     route = get_object_or_404(Route, pk=pk)
#     route.delete()
#     return redirect('route_list')  # Redirige a la lista de rutas después de eliminar

# class RouteUpdateView(UpdateView):
#     model = Route
#     fields = ['name']  # Campos que se pueden editar
#     template_name = 'route_form.html'  # Plantilla del formulario de edición
#     success_url = reverse_lazy('route_list')  # Redirige a la lista de rutas después de editar

# # class RouteDetailView(DetailView):
# #     model = Route
# #     template_name = 'route_detail.html'  # Plantilla que mostrará los detalles de la ruta

@login_required(login_url='inicio_sesion')
def remove_image(request, pk, public_id):
    # Remueve el prefijo de versión en caso de que exista
    if public_id.startswith("v"):
        public_id = "/".join(public_id.split("/")[1:])  # Remover el prefijo de versión, si está presente

    place = get_object_or_404(InterestPlace, pk=pk)
    if request.user != place.creator:
        return redirect('interest_place_edit', pk=pk)
    
    # Eliminar la imagen de Cloudinary
    print(f"Intentando eliminar la imagen con public_id: {public_id}")
    response = destroy(public_id)
    
    if response.get("result") == "ok":
        # Actualizar la lista de imágenes en la base de datos
        place.images = [img for img in place.images if public_id not in img]
        place.save()
        print("Imagen eliminada exitosamente.")
    else:
        print("Error al eliminar la imagen en Cloudinary.")

    return redirect('interest_place_edit', pk=pk) 

# Vista para listar los lugares de interés con paginación
class InterestPlaceListView(LoginRequiredMixin, ListView):
    model = InterestPlace
    template_name = 'interest_places.html'
    context_object_name = 'interest_places'
    paginate_by = 10
    login_url = 'mostrar_formulario_Inicio'  # URL de inicio de sesión si el usuario no está autenticado

# Vista para editar un lugar de interés (requiere autenticación y ser el creador)
class InterestPlaceUpdateView(LoginRequiredMixin, UpdateView):
    model = InterestPlace
    fields = ['name', 'description', 'categories', 'latitude', 'longitude', 'address']
    template_name = 'interestplace_form.html'
    success_url = reverse_lazy('interest_place_list')
    login_url = 'mostrar_formulario_Inicio'

    def dispatch(self, request, *args, **kwargs):
        # Verifica que el usuario sea el creador del lugar de interés
        place = self.get_object()
        if place.creator != request.user:
            return redirect('interest_place_list')  # Redirige si el usuario no es el creador
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        place = form.save(commit=False)

        # Manejo de nuevas imágenes subidas
        new_images = self.request.FILES.getlist('images')
        image_urls = place.images  # Cargar imágenes actuales

        for img in new_images:
            upload_response = upload(img)
            image_urls.append(upload_response['url'])

        place.images = image_urls  # Actualizamos el campo de imágenes
        place.save()  # Guardamos el lugar de interés con las nuevas imágenes

        messages.success(self.request, 'Lugar de interés actualizado correctamente.')
        return redirect(self.success_url)

# Vista para ver un lugar de interés
class InterestPlaceDetailView(LoginRequiredMixin, DetailView):
    model = InterestPlace
    template_name = 'interestplace_detail.html'
    login_url = 'mostrar_formulario_Inicio'

# Vista para listar las rutas con paginación
class RouteListView(LoginRequiredMixin, ListView):
    model = Route
    template_name = 'routes.html'
    context_object_name = 'routes'
    paginate_by = 10
    login_url = 'mostrar_formulario_Inicio'

# Vista para editar una ruta (requiere autenticación y ser el creador)
class RouteUpdateView(LoginRequiredMixin, View):
    login_url = 'mostrar_formulario_Inicio'

    def dispatch(self, request, *args, **kwargs):
        route = get_object_or_404(Route, pk=kwargs['pk'])

        # Verificar si el usuario es el creador de la ruta
        if route.creator != request.user:
            messages.error(request, 'No tienes permiso para editar esta ruta.')
            return redirect('route_list')  # Redirige a la lista de rutas

        return super().dispatch(request, *args, **kwargs)  # Procede si el usuario es el creador

    def get(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        interest_places = InterestPlace.objects.all()  # Todos los lugares de interés
        route_interest_places = route.routeinterestplace_set.all().values_list('interest_place', flat=True)  # Lugares ya seleccionados en la ruta

        # Renderizar el formulario con datos actuales
        return render(request, 'route_edit_form.html', {
            'route': route,
            'interest_places': interest_places,
            'route_interest_places': route_interest_places,
        })

    def post(self, request, pk):
        route = get_object_or_404(Route, pk=pk)
        route.name = request.POST.get('name')
        route.description = request.POST.get('description')
        route.save()

        # Obtener lugares de interés seleccionados
        selected_places = request.POST.getlist('interest_places')

        # Actualizar la relación de lugares de interés en la ruta
        RouteInterestPlace.objects.filter(route=route).exclude(interest_place__id__in=selected_places).delete()  # Eliminar deseleccionados
        for place_id in selected_places:
            place = get_object_or_404(InterestPlace, pk=place_id)
            RouteInterestPlace.objects.get_or_create(route=route, interest_place=place)

        messages.success(request, 'Ruta actualizada con éxito.')
        return redirect('route_list')

# Vista para ver los detalles de una ruta
class RouteDetailView(LoginRequiredMixin, DetailView):
    model = Route
    template_name = 'route_detail.html'
    login_url = 'mostrar_formulario_Inicio'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['interest_places'] = RouteInterestPlace.objects.filter(route=self.object)
        context['route_description'] = self.object.description
        return context

# Vista para eliminar un lugar de interés (requiere autenticación y ser el creador)
@login_required(login_url='mostrar_formulario_Inicio')
def delete_interest_place(request, pk):
    place = get_object_or_404(InterestPlace, pk=pk)
    if place.creator == request.user:
        place.delete()  # Elimina solo si el usuario es el creador
    return redirect('interest_place_list')

# Vista para eliminar una ruta (requiere autenticación y ser el creador)
@login_required(login_url='mostrar_formulario_Inicio')
def delete_route(request, pk):
    route = get_object_or_404(Route, pk=pk)
    if route.creator == request.user:
        route.delete()  # Elimina solo si el usuario es el creador
    return redirect('route_list')

#####################################

# Crear rutas


class RouteForm(ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'description']

class RouteInterestPlaceForm(forms.Form):
    interest_places = ModelMultipleChoiceField(
        queryset=InterestPlace.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Selecciona los lugares de interés para la ruta"
    )

@login_required
def add_route(request):
    if request.method == 'POST':
        route_form = RouteForm(request.POST)
        
        if route_form.is_valid():
            # Crear la nueva ruta
            new_route = route_form.save(commit=False)
            new_route.creator = request.user  # Asigna el creador de la ruta
            new_route.save()

            # Redirige a la selección de lugares de interés
            return redirect(reverse('add_route_interest_places', args=[new_route.id]))
    else:
        route_form = RouteForm()

    return render(request, 'add_route.html', {'route_form': route_form})

@login_required
def add_route_interest_places(request, route_id):
    route = get_object_or_404(Route, id=route_id)

    if request.method == 'POST':
        form = RouteInterestPlaceForm(request.POST)
        if form.is_valid():
            interest_places = form.cleaned_data['interest_places']
            # Asigna los lugares de interés a la ruta
            for place in interest_places:
                RouteInterestPlace.objects.create(route=route, interest_place=place)
            
            messages.success(request, 'Ruta creada con éxito y lugares de interés añadidos.')
            return redirect('route_list')
    else:
        form = RouteInterestPlaceForm()

    return render(request, 'add_route_interest_places.html', {'form': form, 'route': route})