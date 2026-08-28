"""
Aquí vive TODA la lógica de "cuándo sincronizar con Google Calendar".

Antes, cada vista (agendar_cita, confirmar_cita, cancelar_cita,
editar_cita, eliminar_cita, etc.) tenía que acordarse de llamar
manualmente a sincronizar_cita()/eliminar_eventos_cita(). Eso hacía que
la misma lógica estuviera repartida en 3 archivos distintos y era fácil
olvidarla en una vista nueva.

Con estas señales, Django llama automáticamente a esta lógica cada vez
que se guarda (`post_save`) o se borra (`pre_delete`) una Cita, sin
importar desde qué vista, comando o script se haga ese guardado.
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
def _recordar_barbero_anterior(sender, instance, **kwargs):
    """
    Antes de guardar, si la cita ya existía, recuerda quién era el
    barbero anterior. Lo necesitamos en post_save para saber si hubo
    una reasignación y así quitar el evento del calendario viejo.
    """
    if instance.pk:
        anterior = Cita.objects.filter(pk=instance.pk).first()
        instance._barbero_anterior = anterior.barbero if anterior else None
    else:
        instance._barbero_anterior = None


@receiver(post_save, sender=Cita)
def _sincronizar_al_guardar(sender, instance, created, **kwargs):
    barbero_anterior = getattr(instance, "_barbero_anterior", None)

    # Si cambió de barbero, primero se quita del calendario del anterior
    if barbero_anterior and barbero_anterior != instance.barbero:
        eliminar_evento_de_usuario(instance, usuario_de_barbero(barbero_anterior))

    # sincronizar_cita ya decide internamente si debe crear/actualizar
    # el evento (estado activo) o borrarlo (cancelada/finalizada).
    sincronizar_cita(instance)


@receiver(pre_delete, sender=Cita)
def _limpiar_al_borrar(sender, instance, **kwargs):
    eliminar_eventos_cita(instance)
