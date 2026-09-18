from django.urls import path

from . import views

app_name = "notificaciones"

urlpatterns = [
    path("", views.listar_notificaciones, name="listar"),
    path("marcar-leidas/", views.marcar_leidas, name="marcar_leidas"),
    path("vaciar/", views.vaciar_notificaciones, name="vaciar"),
    path("suscribirse-turno/", views.suscribirse_turno, name="suscribirse_turno"),
]
