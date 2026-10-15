"""Notificaciones automáticas relacionadas con la liberación de turnos."""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from citas.models import Cita

from .models import SuscripcionTurno
from .utils import (
    notificar,
    notificar_administradores,
    usuario_de_barbero,
    usuario_de_cliente,
)


@receiver(pre_save, sender=Cita)
def _recordar_estado_anterior(sender, instance, raw=False, **kwargs):
    # Durante loaddata, las relaciones pueden no estar restauradas todavía.
    if raw:
        return

    if instance.pk:
        anterior = Cita.objects.filter(pk=instance.pk).first()
        instance._estado_anterior_notif = (
            anterior.estado if anterior else None
        )
        instance._datos_anteriores_notif = anterior
    else:
        instance._estado_anterior_notif = None
        instance._datos_anteriores_notif = None


@receiver(post_save, sender=Cita)
def _notificar_turno_liberado(
    sender, instance, created, raw=False, **kwargs
):
    # No generar notificaciones mientras Django restaura fixtures.
    if raw:
        return

    estado_anterior = getattr(instance, "_estado_anterior_notif", None)

    # Solo notificar cuando una cita existente pasa a Cancelada.
    if instance.estado != "Cancelada" or estado_anterior == "Cancelada":
        return

    anterior = getattr(instance, "_datos_anteriores_notif", None)

    cliente = anterior.cliente if anterior else instance.cliente
    barbero = anterior.barbero if anterior else instance.barbero
    fecha = anterior.fecha if anterior else instance.fecha
    hora = anterior.hora if anterior else instance.hora
    servicio = anterior.servicio if anterior else instance.servicio

    fecha_legible = fecha.strftime("%d/%m/%Y")
    nombre_barbero = barbero.nombre if barbero else "el barbero"

    mensaje_barbero = (
        f"Tu cita con {cliente.nombre} fue cancelada. "
        f"Este turno quedó libre: {fecha_legible} a las {hora} "
        f"({servicio.nombre})."
    )

    mensaje_disponible = (
        f"El turno del {fecha_legible} a las {hora} con {nombre_barbero} "
        f"({servicio.nombre}) quedó disponible nuevamente."
    )

    # 1. Cliente que tenía la cita.
    usuario_cliente = usuario_de_cliente(cliente)
    notificar(
        usuario_cliente,
        f"Tu cita del {fecha_legible} a las {hora} fue cancelada. "
        f"{mensaje_disponible}",
        cita=instance,
    )

    # 2. Barbero afectado.
    usuario_barbero = usuario_de_barbero(barbero)
    notificar(usuario_barbero, mensaje_barbero, cita=instance)

    # 3. Administradores.
    notificar_administradores(mensaje_disponible, cita=instance)

    # 4. Clientes suscritos al turno liberado.
    suscripciones = SuscripcionTurno.objects.filter(
        barbero=barbero,
        fecha=fecha,
        hora=hora,
    ).exclude(usuario_id=getattr(usuario_cliente, "id", None))

    for suscripcion in suscripciones.select_related("usuario"):
        notificar(
            suscripcion.usuario,
            f"🔔 {mensaje_disponible} Lo estabas siguiendo para recibir un aviso.",
            cita=instance,
        )

    # Las suscripciones se eliminan después de notificar.
    suscripciones.delete()