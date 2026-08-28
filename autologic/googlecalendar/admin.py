from django.contrib import admin

from .models import CitaEventoGoogle, CuentaGoogle


@admin.register(CuentaGoogle)
class CuentaGoogleAdmin(admin.ModelAdmin):
    list_display = ("usuario", "email_google", "fecha_conexion", "fecha_actualizacion")
    search_fields = ("usuario__username", "usuario__email", "email_google")


@admin.register(CitaEventoGoogle)
class CitaEventoGoogleAdmin(admin.ModelAdmin):
    list_display = ("cita", "usuario", "event_id", "calendar_id", "creado")
    search_fields = ("usuario__username", "event_id")
