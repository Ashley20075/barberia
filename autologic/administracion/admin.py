from django.contrib import admin
from .models import Sitio


@admin.register(Sitio)
class SitioAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Marca y portada", {"fields": ("nombre_marca", "eslogan", "hero_titulo", "hero_descripcion", "hero_imagen_1", "hero_imagen_2", "hero_imagen_3")}),
        ("Servicios", {"fields": ("servicios_titulo", "servicios_subtitulo")}),
        ("Barberos", {"fields": ("barberos_titulo", "barberos_subtitulo")}),
        ("Nosotros", {"fields": ("nosotros_titulo", "nosotros_parrafo_1", "nosotros_parrafo_2", "nosotros_punto_1", "nosotros_punto_2", "nosotros_punto_3", "nosotros_imagen")}),
        ("Testimonios", {"fields": ("testimonios_titulo", "testimonios_subtitulo", "testimonio_1", "testimonio_1_autor", "testimonio_2", "testimonio_2_autor", "testimonio_3", "testimonio_3_autor")}),
        ("Llamado a la acción", {"fields": ("cta_titulo", "cta_descripcion", "cta_boton")}),
        ("Pie de página", {"fields": ("footer_descripcion", "horario", "direccion", "telefono", "email", "noticias_titulo", "noticias_descripcion", "copyright_texto")}),
    )
