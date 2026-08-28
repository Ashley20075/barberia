from django.conf import settings
from django.db import models


class CuentaGoogle(models.Model):
    """
    Guarda el token OAuth de Google Calendar de UN usuario (puede ser el
    administrador o un barbero, ambos son instancias de auth.User).
    Cada usuario conecta su propia cuenta desde su panel.
    """

    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="cuenta_google",
    )

    token_acceso = models.TextField()
    token_refresco = models.TextField()
    token_uri = models.CharField(max_length=200, default="https://oauth2.googleapis.com/token")
    client_id = models.CharField(max_length=255)
    client_secret = models.CharField(max_length=255)
    scopes = models.CharField(max_length=500)

    expiracion = models.DateTimeField(null=True, blank=True)

    email_google = models.EmailField(blank=True, default="")
    fecha_conexion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Google Calendar de {self.usuario.username}"

    class Meta:
        verbose_name = "Cuenta de Google conectada"
        verbose_name_plural = "Cuentas de Google conectadas"


class CitaEventoGoogle(models.Model):
    """
    Relaciona una Cita con el evento que se creó en el Google Calendar
    de un usuario específico (puede haber una fila para el admin y otra
    para el barbero asignado, por la misma cita).
    """

    cita = models.ForeignKey(
        "citas.Cita",
        on_delete=models.CASCADE,
        related_name="eventos_google",
    )
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="eventos_google_creados",
    )
    calendar_id = models.CharField(max_length=255, default="primary")
    event_id = models.CharField(max_length=255)

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("cita", "usuario")
        verbose_name = "Evento de Google Calendar por cita"
        verbose_name_plural = "Eventos de Google Calendar por cita"

    def __str__(self):
        return f"Cita #{self.cita_id} -> evento {self.event_id} ({self.usuario.username})"
