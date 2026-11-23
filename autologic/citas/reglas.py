"""Reglas de negocio de las citas: cancelación con antelación y penalizaciones."""
from datetime import timedelta

from django.utils import timezone

# Un cliente solo puede cancelar su cita si faltan al menos estas horas.
HORAS_MIN_CANCELACION = 24

# Penalización por inasistencia del cliente (según cuántas acumula):
#   1.ª falta  -> advertencia
#   2.ª falta  -> no puede agendar por su cuenta durante 7 días
#   3.ª o más  -> no puede agendar por su cuenta durante 15 días
DIAS_PENALIZACION = {1: 0, 2: 7}
DIAS_PENALIZACION_MAXIMA = 15

# Minutos que deben pasar desde el inicio de la cita para poder marcarla
# como "no asistió".
MINUTOS_GRACIA_INASISTENCIA = 15


def dias_de_penalizacion(numero_de_faltas):
    return DIAS_PENALIZACION.get(numero_de_faltas, DIAS_PENALIZACION_MAXIMA)


def horas_para_la_cita(cita, ahora=None):
    inicio = cita.inicio
    if inicio is None:
        return None
    ahora = ahora or timezone.now()
    return (inicio - ahora).total_seconds() / 3600


def puede_cancelar_cliente(cita, ahora=None):
    """True si el cliente aún puede cancelar (≥ 24 h de antelación)."""
    horas = horas_para_la_cita(cita, ahora)
    return horas is not None and horas >= HORAS_MIN_CANCELACION


def puede_marcar_inasistencia(cita, ahora=None):
    """Solo se puede marcar cuando la hora de la cita ya pasó (+ gracia)."""
    inicio = cita.inicio
    if inicio is None:
        return False
    ahora = ahora or timezone.now()
    return ahora >= inicio + timedelta(minutes=MINUTOS_GRACIA_INASISTENCIA)
