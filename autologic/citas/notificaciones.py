"""
Lógica para notificar al barbero y al cliente cuando un turno queda
disponible (por cancelación de cualquiera de las dos partes).
"""

from django.contrib.auth.models import User

from .models import Notificacion


def notificar_cliente_turno_liberado(cita):
    """
    El barbero canceló la cita -> se avisa al cliente que su turno
    quedó libre/cancelado.
    """
    usuario = getattr(cita.cliente, "user", None)

    if not usuario:
        return None

    nombre_barbero = cita.barbero.nombre if cita.barbero else "tu barbero"

    mensaje = (
        f"Tu turno del {cita.fecha.strftime('%d/%m/%Y')} a las {cita.hora} "
        f"con {nombre_barbero} fue cancelado y quedó liberado."
    )

    return Notificacion.objects.create(
        usuario=usuario,
        cita=cita,
        tipo="cita_cancelada",
        mensaje=mensaje,
    )


def notificar_barbero_turno_liberado(cita):
    """
    El cliente canceló la cita -> se avisa al barbero que ese
    horario quedó libre en su agenda.
    """
    if not cita.barbero or not cita.barbero.email:
        return None

    usuario = User.objects.filter(email=cita.barbero.email).first()

    if not usuario:
        return None

    mensaje = (
        f"{cita.cliente.nombre} canceló su cita. El turno del "
        f"{cita.fecha.strftime('%d/%m/%Y')} a las {cita.hora} quedó libre."
    )

    return Notificacion.objects.create(
        usuario=usuario,
        cita=cita,
        tipo="turno_liberado",
        mensaje=mensaje,
    )
