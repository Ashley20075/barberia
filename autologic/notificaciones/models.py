from django.conf import settings
from django.db import models


class Notificacion(models.Model):
    """
    Aviso persistente para un usuario (cliente o barbero). A diferencia
    de los `messages` de Django (que solo se ven una vez, justo después
    de la acción de quien la ejecuta), esto queda guardado para que la
    OTRA persona involucrada también se entere — por ejemplo, si el
    barbero cancela una cita, el cliente debe enterarse aunque no haya
    sido quien hizo la acción.
    """

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones",
    )
    mensaje = models.CharField(max_length=255)
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
