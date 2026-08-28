from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path(
        'notificaciones/leer/<int:id>/',
        views.marcar_notificacion_leida,
        name='marcar_notificacion_leida'
    ),
    path(
        'notificaciones/leer-todas/',
        views.marcar_todas_notificaciones_leidas,
        name='marcar_todas_notificaciones_leidas'
    ),
]