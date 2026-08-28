from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from citas.models import Notificacion, Servicio


def inicio(request):

    servicios = Servicio.objects.all().order_by("id")

    return render(
        request,
        "index.html",
        {
            "servicios": servicios
        }
    )


@login_required(login_url='login')
def marcar_notificacion_leida(request, id):
    notificacion = get_object_or_404(
        Notificacion,
        id=id,
        usuario=request.user
    )

    notificacion.leida = True
    notificacion.save()

    siguiente = request.POST.get("next") or request.META.get("HTTP_REFERER")

    return redirect(siguiente or "inicio")


@login_required(login_url='login')
def marcar_todas_notificaciones_leidas(request):
    Notificacion.objects.filter(
        usuario=request.user,
        leida=False
    ).update(leida=True)

    siguiente = request.POST.get("next") or request.META.get("HTTP_REFERER")

    return redirect(siguiente or "inicio")