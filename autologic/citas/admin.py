from django.contrib import admin
from .models import Cita, Barbero, Resena, Servicio, SuscriptorNewsletter

admin.site.register(Cita)
admin.site.register(Barbero)
admin.site.register(Servicio)


@admin.register(SuscriptorNewsletter)
class SuscriptorNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'creado')
    search_fields = ('email',)
    ordering = ('-creado',)


@admin.register(Resena)
class ResenaAdmin(admin.ModelAdmin):
    list_display = ("cita", "puntuacion", "creada")
    list_filter = ("puntuacion",)
