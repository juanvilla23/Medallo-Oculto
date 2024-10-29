
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponse
from users.models import Promotor,Turista
from django.contrib.auth.decorators import login_required




def mostrar_formulario_Inicio(request):
    return render(request,'Inicio.html')

def inicio_sesion(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)
        if user is not None: # si el usuario no esta en la base de datos la variable toma el valor de None
            if user.is_active:
                login(request, user) #se guarda la informacion en login 
                return redirect('mostrar_perfil')  # Redirige a la página de inicio
            else:
                error="El usuario no esta activo "
                return render(request, 'Inicio.html', {'error': error})
        else:
            error="Usuario y contraseña incorrectos "
            return render(request, 'Inicio.html', {'error': error})
            

    # Si la solicitud no es POST, muestra el formulario vacío
    return render(request, 'register.html')

def crear_cuenta_form(request):
    return render(request,'formCrearCuenta.html')



def crear_cuenta(request):
    if request.method=="POST":
        username = request.POST.get('username')
        tipo_usuario=request.POST.get('tipo_usuario')
        password = request.POST.get('password')
        password2= request.POST.get('confirm_password')
        print(f"password: {password}")
        print(f"password2: {password2}")

        if password!=password2:
            error="Contraseñas diferentes"
            print(error)
            return render(request, 'formCrearCuenta.html', {'error': error})
        else:
            if User.objects.filter(username=username).exists():
                error = "El nombre de usuario ya existe. Elige otro nombre."
                print(error)
                return render(request, 'formCrearCuenta.html', {'error': error})
            else:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                print("creando usuario")
                # Crear el tipo de usuario según la elección
                if tipo_usuario == 'Promotor':
                    Promotor.objects.create(user=user)  # Crea un Promotor asociado al usuario
                elif tipo_usuario == 'Turista':
                    Turista.objects.create(user=user)  # Crea un Turista asociado al usuario

                # Autenticar y loguear al usuario automáticamente
                login(request, user)
                return redirect('mostrar_formulario_Inicio')
    else:            
        return render(request, 'formCrearCuenta.html')
@login_required
def mostar_perfil(request):
    # Obtén el usuario autenticado
    usuario = request.user
    #print(request.user.tipo)
    print(usuario)

    # Si tienes modelos específicos como Promotor o Turista asociados, puedes verificarlos aquí:
    es_promotor = hasattr(usuario, 'promotor')
    es_turista = hasattr(usuario, 'turista')

    # Datos específicos según el tipo de usuario
    datos_usuario = None
    if es_promotor:
        promotor = usuario.promotor
        datos_usuario = {
            'tipo': promotor.tipo,
            'id':promotor.id,
            'telefono': promotor.telefono,
        }
    elif es_turista:
        Turista = usuario.turista
        datos_usuario = {
            'tipo': Turista.tipo,
            'id':Turista.id
        }

    # Renderiza la plantilla con la información del usuario
    return render(request, 'perfil.html', {
        'usuario': usuario,
        'datos_usuario': datos_usuario,
        'es_promotor': es_promotor,
        'es_turista': es_turista,
    })









