from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('recuperar-contrasena/', views.recuperar_contrasena, name='recuperar_contrasena'),
    path(
    "cambiar-contrasena/",
    views.cambiar_contrasena,
    name="cambiar_contrasena",
),
]