"""
Funciones de apoyo para conectar y sincronizar citas con Google Calendar.

Nada de este archivo detiene el flujo normal de citas si algo falla: si un
usuario no ha conectado su Google Calendar, o si la llamada a la API de
Google falla, simplemente no se crea/actualiza el evento, pero la cita en
la base de datos siempre queda guardada con normalidad.
"""

import datetime
import logging

from django.conf import settings
from django.contrib.auth.models import User
from django.utils import timezone

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from .models import CitaEventoGoogle, CuentaGoogle

logger = logging.getLogger(__name__)

ZONA_HORARIA = "America/Bogota"

# Estados de Cita que SÍ deben mostrarse como evento activo en el calendario
ESTADOS_ACTIVOS = ("Pendiente", "Confirmada")


def _credenciales_desde_cuenta(cuenta: CuentaGoogle) -> Credentials:
    return Credentials(
        token=cuenta.token_acceso,
        refresh_token=cuenta.token_refresco,
        token_uri=cuenta.token_uri,
        client_id=cuenta.client_id,
        client_secret=cuenta.client_secret,
        scopes=cuenta.scopes.split(","),
    )


def obtener_servicio_calendar(usuario: User):
    """
    Devuelve un cliente de la API de Google Calendar ya autenticado para
    el `usuario` dado, o None si ese usuario no ha conectado su cuenta
    (o si el token ya no sirve y no se pudo refrescar).
    """

    try:
        cuenta = usuario.cuenta_google
    except CuentaGoogle.DoesNotExist:
        return None

    credenciales = _credenciales_desde_cuenta(cuenta)

    if credenciales.expired and credenciales.refresh_token:
        try:
            credenciales.refresh(Request())
            cuenta.token_acceso = credenciales.token
            cuenta.expiracion = credenciales.expiry
            cuenta.save(update_fields=["token_acceso", "expiracion", "fecha_actualizacion"])
        except Exception:
            logger.exception("No se pudo refrescar el token de Google de %s", usuario)
            return None

    try:
        return build("calendar", "v3", credentials=credenciales, cache_discovery=False)
    except Exception:
        logger.exception("No se pudo construir el servicio de Calendar para %s", usuario)
        return None


def _parsear_inicio_fin(cita):
    hora_obj = datetime.datetime.strptime(cita.hora, "%I:%M %p").time()
    inicio = datetime.datetime.combine(cita.fecha, hora_obj)
    duracion = cita.duracion_total or 35
    fin = inicio + datetime.timedelta(minutes=duracion)
    return inicio, fin


def _cuerpo_evento(cita) -> dict:
    inicio, fin = _parsear_inicio_fin(cita)
    nombre_barbero = cita.barbero.nombre if cita.barbero else "Sin asignar"

    descripcion_lineas = [
        f"Cliente: {cita.cliente.nombre}",
        f"Servicio: {cita.servicio.nombre}",
        f"Barbero: {nombre_barbero}",
        f"Estado: {cita.estado}",
    ]
    if cita.adicionales and cita.adicionales != "Ninguno":
        descripcion_lineas.append(f"Adicionales: {cita.adicionales}")
    if cita.productos and cita.productos != "Ninguno":
        descripcion_lineas.append(f"Productos: {cita.productos}")

    return {
        "summary": f"Cita {cita.cliente.nombre} - {nombre_barbero}",
        "description": "\n".join(descripcion_lineas),
        "start": {"dateTime": inicio.isoformat(), "timeZone": ZONA_HORARIA},
        "end": {"dateTime": fin.isoformat(), "timeZone": ZONA_HORARIA},
    }


def _crear_o_actualizar_para_usuario(cita, usuario: User):
    servicio = obtener_servicio_calendar(usuario)
    if servicio is None:
        return

    cuerpo = _cuerpo_evento(cita)
    registro = CitaEventoGoogle.objects.filter(cita=cita, usuario=usuario).first()

    try:
        if registro:
            servicio.events().update(
                calendarId=registro.calendar_id,
                eventId=registro.event_id,
                body=cuerpo,
            ).execute()
        else:
            evento = servicio.events().insert(calendarId="primary", body=cuerpo).execute()
            CitaEventoGoogle.objects.create(
                cita=cita,
                usuario=usuario,
                calendar_id="primary",
                event_id=evento["id"],
            )
    except HttpError as error:
        if error.resp is not None and error.resp.status == 404 and registro:
            # El evento fue borrado manualmente en Google Calendar: lo recreamos
            registro.delete()
            _crear_o_actualizar_para_usuario(cita, usuario)
        else:
            logger.exception("Error de Google Calendar al sincronizar cita %s", cita.id)


def _eliminar_para_usuario(cita, usuario: User):
    registro = CitaEventoGoogle.objects.filter(cita=cita, usuario=usuario).first()
    if not registro:
        return

    servicio = obtener_servicio_calendar(usuario)
    if servicio is not None:
        try:
            servicio.events().delete(
                calendarId=registro.calendar_id,
                eventId=registro.event_id,
            ).execute()
        except HttpError as error:
            if error.resp is None or error.resp.status not in (404, 410):
                logger.exception("Error al eliminar evento de Google Calendar para cita %s", cita.id)

    registro.delete()


def _usuario_admin_conectados():
    return User.objects.filter(is_superuser=True, cuenta_google__isnull=False)


def _usuario_barbero(cita):
    if not cita.barbero:
        return None
    return User.objects.filter(email=cita.barbero.email).first()


def sincronizar_cita(cita):
    """
    Crea o actualiza el evento de esta cita en:
      - el calendario de cada administrador conectado
      - el calendario del barbero asignado, si tiene cuenta conectada

    Debe llamarse cada vez que una cita se crea, o cambia de barbero,
    fecha, hora, servicio o pasa a un estado activo (Pendiente/Confirmada).
    """

    if cita.estado not in ESTADOS_ACTIVOS:
        eliminar_eventos_cita(cita)
        return

    for admin in _usuario_admin_conectados():
        _crear_o_actualizar_para_usuario(cita, admin)

    barbero_user = _usuario_barbero(cita)
    if barbero_user:
        _crear_o_actualizar_para_usuario(cita, barbero_user)


def usuario_de_barbero(barbero):
    """Devuelve el User (cuenta de login) que corresponde a un Barbero, si existe."""
    if not barbero:
        return None
    return User.objects.filter(email=barbero.email).first()


def eliminar_evento_de_usuario(cita, usuario):
    """
    Borra (si existe) SOLO el evento de Google Calendar de `usuario` para
    esta cita. Útil cuando una cita se reasigna a otro barbero: hay que
    quitarla del calendario del barbero anterior sin tocar el del admin.
    """
    if usuario is None:
        return
    _eliminar_para_usuario(cita, usuario)


def eliminar_eventos_cita(cita):
    """
    Borra de Google Calendar todos los eventos asociados a esta cita
    (admin y barbero). Debe llamarse cuando una cita se cancela, se
    finaliza o se elimina.
    """

    for registro in list(cita.eventos_google.all()):
        _eliminar_para_usuario(cita, registro.usuario)
