from django.urls import path

from . import views

app_name = "notificaciones"

urlpatterns = [
    path("", views.listar_notificaciones, name="listar"),
    path("marcar-leidas/", views.marcar_leidas, name="marcar_leidas"),
]
