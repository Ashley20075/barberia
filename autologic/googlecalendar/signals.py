
"""
Aquí vive TODA la lógica de cuándo sincronizar con Google Calendar.
"""

from django.db.models.signals import post_save, pre_delete, pre_save
from django.dispatch import receiver

from citas.models import Cita

from .utils import (
    eliminar_eventos_cita,
    eliminar_evento_de_usuario,
    sincronizar_cita,
    usuario_de_barbero,
)


@receiver(pre_save, sender=Cita)
def _recordar_barbero_anterior(sender, instance, raw=False, **kwargs):
    """
    Recuerda el barbero anterior antes de guardar una cita.
    Durante la carga de fixtures no consulta relaciones incompletas.
    """
    if raw:
        return

    if instance.pk:
        anterior = Cita.objects.filter(pk=instance.pk).first()
        instance._barbero_anterior = (
            anterior.barbero if anterior else None
        )
    else:
        instance._barbero_anterior = None


@receiver(post_save, sender=Cita)
def _sincronizar_al_guardar(
    sender, instance, created, raw=False, **kwargs
):
    # No sincronizar con Google Calendar durante loaddata.
    if raw:
        return

    barbero_anterior = getattr(instance, "_barbero_anterior", None)

    # Si cambió de barbero, quitar el evento del calendario anterior.
    if barbero_anterior and barbero_anterior != instance.barbero:
        eliminar_evento_de_usuario(
            instance,
            usuario_de_barbero(barbero_anterior),
        )

    # Mantener la sincronización normal de citas.
    sincronizar_cita(instance)


@receiver(pre_delete, sender=Cita)
def _limpiar_al_borrar(sender, instance, raw=False, **kwargs):
    # No realizar operaciones externas durante la carga de fixtures.
    if raw:
        return

    eliminar_eventos_cita(instance)