from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),

    path('', include('usuarios.urls')),
    path('', include('clientes.urls')),
    path('', include('barberos.urls')),
    path('', include('citas.urls')),
    path('', include('administracion.urls')),

    path(
        'inventario/',
        include('inventario.urls')
    ),

    path(
        'calendario/',
        include('googlecalendar.urls')
    ),

    path(
        'notificaciones/',
        include('notificaciones.urls')
    ),

    path(
        'ia-estilo/',
        include('ia_estilo.urls')
    ),
]