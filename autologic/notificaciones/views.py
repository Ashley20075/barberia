from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render

from barberos.models import Barbero

from .models import Notificacion, SuscripcionTurno


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
def vaciar_notificaciones(request):
    """Elimina todas las notificaciones del usuario autenticado."""
    if request.method != "POST":
        return redirect("notificaciones:listar")

    request.user.notificaciones.all().delete()
    messages.success(request, "✅ Tus notificaciones fueron vaciadas correctamente.")
    siguiente = request.POST.get("next") or "/"
    return redirect(siguiente)


@login_required
def marcar_leidas(request):
    request.user.notificaciones.filter(leida=False).update(leida=True)
    siguiente = request.POST.get("next") or request.GET.get("next") or "/"
    return redirect(siguiente)


@login_required
def suscribirse_turno(request):
    """Activa o desactiva el aviso para un turno concreto."""
    if request.method != "POST":
        return JsonResponse({"ok": False, "error": "Método no permitido."}, status=405)

    if not hasattr(request.user, "cliente"):
        return JsonResponse({"ok": False, "error": "Solo los clientes pueden suscribirse a turnos."}, status=403)

    barbero_id = request.POST.get("barbero")
    fecha = request.POST.get("fecha")
    hora = request.POST.get("hora")
    suscrito = request.POST.get("suscrito") == "true"
    try:
        duracion = int(request.POST.get("duracion_total", 35))
    except (TypeError, ValueError):
        duracion = 35

    if not all([barbero_id, fecha, hora]):
        return JsonResponse({"ok": False, "error": "Faltan datos del turno."}, status=400)

    try:
        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()
    except ValueError:
        return JsonResponse({"ok": False, "error": "Fecha inválida."}, status=400)

    try:
        barbero = Barbero.objects.get(id=barbero_id, activo=True)
    except Barbero.DoesNotExist:
        return JsonResponse({"ok": False, "error": "Barbero inválido."}, status=404)

    if suscrito:
        # La suscripción puede hacerse precisamente sobre un horario ocupado:
        # el objetivo es avisar al cliente cuando ese bloque vuelva a liberarse.
        import datetime as dt

        if not barbero.es_dia_laboral(fecha_obj) or barbero.es_dia_descanso(fecha_obj):
            return JsonResponse(
                {"ok": False, "error": "Ese día no corresponde a una jornada laboral del barbero."},
                status=409,
            )

        try:
            hora_obj = dt.datetime.strptime(hora, "%I:%M %p").time()
        except ValueError:
            return JsonResponse({"ok": False, "error": "Hora inválida."}, status=400)

        inicio_jornada = barbero.jornada_inicio
        fin_jornada = barbero.jornada_fin
        minutos_desde_inicio = (hora_obj.hour * 60 + hora_obj.minute) - (inicio_jornada.hour * 60 + inicio_jornada.minute)
        duracion_jornada = (fin_jornada.hour * 60 + fin_jornada.minute) - (inicio_jornada.hour * 60 + inicio_jornada.minute)

        if minutos_desde_inicio < 0 or minutos_desde_inicio % 15 != 0 or minutos_desde_inicio + duracion > duracion_jornada:
            return JsonResponse({"ok": False, "error": "Ese horario no pertenece a un turno válido."}, status=409)

        SuscripcionTurno.objects.get_or_create(
            usuario=request.user,
            barbero=barbero,
            fecha=fecha_obj,
            hora=hora,
        )
        return JsonResponse({"ok": True, "suscrito": True})

    SuscripcionTurno.objects.filter(
        usuario=request.user,
        barbero=barbero,
        fecha=fecha_obj,
        hora=hora,
    ).delete()
    return JsonResponse({"ok": True, "suscrito": False})
