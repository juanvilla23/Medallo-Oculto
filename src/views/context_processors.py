# events/context_processors.py
from .models import Event

def user_events(request):
    # Inicializa variables predeterminadas
    events2 = []
    es_creador = False
    es_promotor = False

    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        # Filtra los eventos creados por el usuario actual
        events2 = Event.objects.filter(creator=request.user)
        es_creador = events2.exists()  # `True` si el usuario tiene eventos, `False` de lo contrario
        
        # Verifica si el usuario es un promotor
        es_promotor = getattr(request.user, 'user_type', '') == 'promotor'

    return {
        'events2': events2,
        'es_creador': es_creador,
        'es_promotor': es_promotor,
    }
