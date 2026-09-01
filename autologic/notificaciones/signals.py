"""
Aquí vive la lógica de "cuándo avisar que un turno se liberó".

Igual que en googlecalendar/signals.py, usamos señales de Django para
que esto se dispare automáticamente sin importar desde qué vista se
cancele la cita (cliente, barbero o admin) — así no hay que acordarse
de notificar manualmente en cada uno de esos 3 lugares.
"""

from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

from citas.models import Cita

from .utils import notificar, usuario_de_barbero, usuario_de_cliente


@receiver(pre_save, sender=Cita)
def _recordar_estado_anterior(sender, instance, **kwargs):
    if instance.pk:
        anterior = Cita.objects.filter(pk=instance.pk).first()
        instance._estado_anterior_notif = anterior.estado if anterior else None
    else:
        instance._estado_anterior_notif = None


@receiver(post_save, sender=Cita)
def _notificar_turno_liberado(sender, instance, created, **kwargs):
    estado_anterior = getattr(instance, "_estado_anterior_notif", None)

    # Solo notificamos en el momento EXACTO en que la cita pasa a
    # "Cancelada" (el turno se libera). Si ya nacía cancelada o si se
    # guarda de nuevo sin cambiar de estado, no se repite el aviso.
    if instance.estado != "Cancelada" or estado_anterior == "Cancelada":
        return

    fecha_legible = instance.fecha.strftime("%d/%m/%Y")

    usuario_cliente = usuario_de_cliente(instance.cliente)
    usuario_barbero = usuario_de_barbero(instance.barbero)

    notificar(
        usuario_cliente,
        f"Tu cita del {fecha_legible} a las {instance.hora} ({instance.servicio.nombre}) fue cancelada.",
        cita=instance,
    )

    notificar(
        usuario_barbero,
        f"Se liberó un turno: {fecha_legible} a las {instance.hora} "
        f"({instance.servicio.nombre}). Ya puedes ofrecerlo a otro cliente.",
        cita=instance,
    )
