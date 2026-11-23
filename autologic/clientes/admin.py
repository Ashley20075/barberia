from django.contrib import admin

from .models import Cliente


@admin.register(Cliente)
class ClienteAdmin(admin.ModelAdmin):
    list_display = (
        "nombre",
        "email",
        "telefono",
        "cortes_completados",
        "cortes_para_recompensa",
        "recompensas_disponibles",
        "inasistencias",
        "penalizado_hasta",
        "activo",
    )
    search_fields = ("nombre", "email", "cedula", "telefono")
    list_filter = ("activo",)