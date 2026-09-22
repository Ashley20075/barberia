from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from citas.models import Servicio, SuscriptorNewsletter
from barberos.models import Barbero
from administracion.models import Sitio


def inicio(request):

    if request.method == "POST" and request.POST.get("suscripcion_email"):
        email = request.POST.get("suscripcion_email", "").strip()

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, '❌ "%s" no es un correo válido.' % email)
        else:
            _, creado = SuscriptorNewsletter.objects.get_or_create(email__iexact=email, defaults={"email": email})
            if creado:
                messages.success(request, "✅ ¡Listo! Te avisaremos de nuestras novedades.")
            else:
                messages.info(request, "Ese correo ya estaba suscrito.")

        return redirect("inicio")

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
