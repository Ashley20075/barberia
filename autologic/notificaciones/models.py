from django.conf import settings
from django.db import models


class Notificacion(models.Model):
    """Aviso persistente para un usuario."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones",
    )
    mensaje = models.TextField()
    cita = models.ForeignKey(
        "citas.Cita",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificaciones",
    )
    leida = models.BooleanField(default=False)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"{self.usuario.username}: {self.mensaje[:40]}"


class SuscripcionTurno(models.Model):
    """Cliente que quiere ser avisado cuando se libere un turno concreto."""

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="suscripciones_turnos",
    )
    barbero = models.ForeignKey(
        "barberos.Barbero",
        on_delete=models.CASCADE,
        related_name="suscripciones_turnos",
    )
    fecha = models.DateField()
    hora = models.CharField(max_length=20)
    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["fecha", "hora"]
        constraints = [
            models.UniqueConstraint(
                fields=["usuario", "barbero", "fecha", "hora"],
                name="unique_suscripcion_turno_usuario",
            )
        ]
        verbose_name = "Suscripción a turno"
        verbose_name_plural = "Suscripciones a turnos"

    def __str__(self):
        return f"{self.usuario.username} - {self.barbero.nombre} - {self.fecha} {self.hora}"
