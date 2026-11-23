"""Calificación del servicio por parte del cliente."""
from decimal import ROUND_HALF_UP, Decimal

from django.db import transaction

from notificaciones.utils import notificar, notificar_administradores, usuario_de_barbero


def registrar_resena(cita, puntuacion, comentario=""):
    """
    Guarda la reseña de una cita finalizada (una sola por cita), actualiza el
    promedio del barbero y le avisa. Devuelve la reseña, o None si no aplica.
    """
    from barberos.models import Barbero
    from .models import Resena

    comentario = (comentario or "").strip()[:500]
    with transaction.atomic():
        if cita.estado != "Finalizada" or Resena.objects.filter(cita=cita).exists():
            return None
        resena = Resena.objects.create(cita=cita, puntuacion=puntuacion, comentario=comentario)

        if cita.barbero_id:
            barbero = Barbero.objects.select_for_update().get(pk=cita.barbero_id)
            total = Decimal(barbero.calificacion) * barbero.numero_resenas + puntuacion
            barbero.numero_resenas += 1
            barbero.calificacion = (total / barbero.numero_resenas).quantize(
                Decimal("0.1"), rounding=ROUND_HALF_UP)
            barbero.save(update_fields=["calificacion", "numero_resenas"])

            texto = f"⭐ {cita.cliente.nombre} calificó tu servicio con {puntuacion}/5."
            if comentario:
                texto += f" Comentario: «{comentario}»"
            notificar(usuario_de_barbero(barbero), texto, cita=cita)
            if puntuacion <= 2:
                notificar_administradores(
                    f"⭐ Calificación baja ({puntuacion}/5) de {cita.cliente.nombre} para {barbero.nombre}.",
                    cita=cita)
    return resena
