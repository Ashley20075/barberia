from django.shortcuts import render
from citas.models import Servicio
from barberos.models import Barbero
from administracion.models import Sitio


def inicio(request):
    servicios = Servicio.objects.all().order_by("id")
    sitio = Sitio.obtener()
    barberos = Barbero.objects.filter(activo=True).order_by("nombre")

    return render(request, "index.html", {
        "servicios": servicios,
        "sitio": sitio,
        "barberos_inicio": barberos,
        "testimonios": [
            (sitio.testimonio_1, sitio.testimonio_1_autor),
            (sitio.testimonio_2, sitio.testimonio_2_autor),
            (sitio.testimonio_3, sitio.testimonio_3_autor),
        ],
    })
