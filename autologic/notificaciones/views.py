from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from barberos.models import Barbero

from .models import Notificacion


@login_required
def listar_notificaciones(request):
    notificaciones = request.user.notificaciones.all()[:50]
    request.user.notificaciones.filter(leida=False).update(leida=True)
    es_barbero = Barbero.objects.filter(email=request.user.email, activo=True).exists()
    return render(
        request,
        "notificaciones/listar.html",
        {"notificaciones": notificaciones, "es_barbero": es_barbero},
    )


@login_required
def marcar_leidas(request):
    request.user.notificaciones.filter(leida=False).update(leida=True)
    siguiente = request.POST.get("next") or request.GET.get("next") or "/"
    return redirect(siguiente)
