from django.urls import path

from . import views

app_name = "googlecalendar"

urlpatterns = [
    path("conectar/", views.conectar_google, name="conectar"),
    path("login-google/", views.iniciar_sesion_google, name="login_google"),
    path("oauth2callback/", views.oauth2callback, name="oauth2callback"),
    path("desconectar/", views.desconectar_google, name="desconectar"),
]
