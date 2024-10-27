from django.urls import path 
from . import views

urlpatterns=[
    path('iniciar_sesion/',views.inicio_sesion,name='inicio_sesion'),
    path('',views.mostrar_formulario_Inicio,name='mostrar_formulario_Inicio'),
    path('crear_cuenta_form/',views.crear_cuenta_form, name='crear_cuenta_form'),
    path('crear_cuenta/',views.crear_cuenta,name='crear_cuenta'),
    path('perfil/',views.mostar_perfil,name='mostrar_perfil'),


    #path('cerrar/',views.cerrar_sesion,name='cerrar_sesion'),
]