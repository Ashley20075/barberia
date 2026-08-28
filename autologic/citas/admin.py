from django.contrib import admin
from .models import Cita, Barbero, Notificacion, Servicio

admin.site.register(Cita)
admin.site.register(Barbero)
admin.site.register(Servicio)


@admin.register(Notificacion)
class NotificacionAdmin(admin.ModelAdmin):
    list_display = ("usuario", "tipo", "mensaje", "leida", "fecha_creacion")
    list_filter = ("tipo", "leida")
    search_fields = ("usuario__username", "usuario__email", "mensaje")