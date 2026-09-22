from django.contrib import admin
from .models import Cita, Barbero, Servicio, SuscriptorNewsletter

admin.site.register(Cita)
admin.site.register(Barbero)
admin.site.register(Servicio)


@admin.register(SuscriptorNewsletter)
class SuscriptorNewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'creado')
    search_fields = ('email',)
    ordering = ('-creado',)