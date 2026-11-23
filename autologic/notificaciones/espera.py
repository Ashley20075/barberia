"""
Lista de espera de turnos.

Un cliente puede ponerse en la lista de espera de un turno ocupado. Si la cita
se cancela, el primero de la fila (por orden de llegada) que cumpla las reglas
queda agendado automáticamente; los demás siguen esperando.
Las suscripciones sin servicio (avisos antiguos) solo reciben una notificación.
"""
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.utils import timezone

from .models import SuscripcionTurno
from .utils import notificar, usuario_de_barbero


def _intentar_asignar(s, cita_origen):
    """Agenda al suscriptor. Devuelve (cita, None) si lo logró o (None, motivo)."""
    from citas.models import Cita
    from clientes.models import Cliente

    cliente = Cliente.objects.filter(user=s.usuario).first()
    if cliente is None:
        return None, "tu cuenta no tiene perfil de cliente"
    if cliente.penalizado:
        return None, (
            "estás penalizado por inasistencias hasta el "
            f"{cliente.penalizado_hasta.strftime('%d/%m/%Y')}"
        )
    try:
        inicio = datetime.strptime(s.hora, "%I:%M %p")
    except ValueError:
        return None, "la hora del turno no es válida"
    if timezone.make_aware(datetime.combine(s.fecha, inicio.time())) <= timezone.now():
        return None, "el turno ya pasó"
    barbero = s.barbero
    if not barbero.activo or not barbero.es_barbero or not barbero.es_dia_laboral(s.fecha):
        return None, "el barbero no atiende en esa fecha"
    if Cita.objects.filter(cliente=cliente, fecha=s.fecha,
                           estado__in=["Pendiente", "Confirmada"]).exists():
        return None, "ya tienes otra cita ese día"

    fin_nueva = inicio + timedelta(minutes=s.duracion_total)
    for otra in Cita.objects.filter(barbero=barbero, fecha=s.fecha,
                                    estado__in=["Pendiente", "Confirmada"]):
        try:
            ini = datetime.strptime(otra.hora, "%I:%M %p")
        except ValueError:
            continue
        if inicio < ini + timedelta(minutes=otra.duracion_total) and fin_nueva > ini:
            return None, "el horario se cruza con otra cita"

    try:
        cita = Cita.objects.create(
            cliente=cliente, servicio=s.servicio, barbero=barbero,
            adicionales=s.adicionales or "Ninguno", productos="Ninguno",
            fecha=s.fecha, hora=s.hora, duracion_total=s.duracion_total,
            estado="Pendiente",
        )
    except ValidationError as e:
        return None, e.messages[0]
    return cita, None


def atender_lista_espera(barbero, fecha, hora, excluir_usuario_id, mensaje_disponible, cita_origen):
    subs = list(
        SuscripcionTurno.objects
        .filter(barbero=barbero, fecha=fecha, hora=hora)
        .exclude(usuario_id=excluir_usuario_id)
        .select_related("usuario", "servicio", "barbero")
        .order_by("creada", "id")
    )
    fecha_legible = fecha.strftime("%d/%m/%Y")
    asignada = None

    for s in subs:
        if s.servicio_id is None:
            notificar(
                s.usuario,
                f"🔔 {mensaje_disponible} Lo estabas siguiendo para recibir un aviso.",
                cita=cita_origen,
            )
            s.delete()
            continue

        if asignada is not None:
            notificar(
                s.usuario,
                f"🕒 Lista de espera: el turno del {fecha_legible} a las {hora} con "
                f"{barbero.nombre} lo tomó otra persona que estaba antes en la fila. "
                "Sigues en la lista por si se vuelve a liberar.",
                cita=cita_origen,
            )
            continue

        cita, motivo = _intentar_asignar(s, cita_origen)
        if cita is None:
            notificar(
                s.usuario,
                f"🕒 Lista de espera: el turno del {fecha_legible} a las {hora} se liberó, "
                f"pero no pudimos agendarlo automáticamente porque {motivo}. "
                "Te sacamos de la lista; puedes reservarlo tú si sigue disponible.",
                cita=cita_origen,
            )
            s.delete()
            continue

        asignada = cita
        notificar(
            s.usuario,
            f"🕒 Lista de espera: se liberó el turno del {fecha_legible} a las {hora} con "
            f"{barbero.nombre} y te lo asignamos ({s.servicio.nombre}). "
            "Tu cita quedó pendiente de confirmación.",
            cita=cita,
        )
        notificar(
            usuario_de_barbero(barbero),
            f"🆕 Nueva cita (desde la lista de espera): {cita.cliente.nombre} el "
            f"{fecha_legible} a las {hora}. Servicio: {s.servicio.nombre}.",
            cita=cita,
        )
        s.delete()
