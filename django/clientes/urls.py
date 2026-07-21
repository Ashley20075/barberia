from django.urls import path
from . import views

urlpatterns = [
    path('cliente/', views.panel_cliente, name='panel_cliente'),
    path('cliente/agendar/', views.agendar_cita, name='agendar_cita'),
    path('cliente/cancelar/<int:id>/', views.cancelar_cita_cliente, name='cancelar_cita_cliente'),
    path('cliente/editar-perfil/', views.editar_perfil, name='editar_perfil'),

    path('eliminar-cuenta/', views.eliminar_cuenta, name='eliminar_cuenta'),
    path('cuenta-eliminada/', views.cuenta_eliminada, name='cuenta_eliminada'),

    path('registro/', views.registro, name='registro'),
    path('logout/', views.logout_view, name='logout'),
]