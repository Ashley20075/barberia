from datetime import datetime, timedelta
from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from barberos.models import Barbero
from clientes.models import Cliente


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio = models.PositiveIntegerField()
    duracion = models.PositiveIntegerField(
        help_text="Duración en minutos"
    )

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Confirmada", "Confirmada"),
        ("Cancelada", "Cancelada"),
        ("Finalizada", "Finalizada"),
    ]

    cliente = models.ForeignKey(
        Cliente,
        on_delete=models.CASCADE,
        related_name="citas"
    )

    servicio = models.ForeignKey(
        Servicio,
        on_delete=models.CASCADE
    )

    barbero = models.ForeignKey(
        Barbero,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="citas"
    )

    adicionales = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    productos = models.CharField(
        max_length=200,
        blank=True,
        default=""
    )

    fecha = models.DateField()

    hora = models.CharField(
        max_length=20
    )

    duracion_total = models.PositiveIntegerField(default=35)

    recordatorio_enviado = models.BooleanField(default=False)

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Pendiente"
    )

    class Meta:
        ordering = ["fecha", "hora"]

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        nombre_barbero = (
            self.barbero.nombre
            if self.barbero
            else "Sin asignar"
        )

        return (
            f"{self.cliente.nombre} - "
            f"{self.fecha} {self.hora} - "
            f"{nombre_barbero}"
        )


class Notificacion(models.Model):
    TIPOS = [
        ("turno_liberado", "Turno liberado"),
        ("cita_cancelada", "Cita cancelada"),
    ]

    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notificaciones"
    )

    cita = models.ForeignKey(
        Cita,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="notificaciones"
    )

    tipo = models.CharField(
        max_length=30,
        choices=TIPOS,
        default="turno_liberado"
    )

    mensaje = models.CharField(max_length=255)

    leida = models.BooleanField(default=False)

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-fecha_creacion"]
        verbose_name = "Notificación"
        verbose_name_plural = "Notificaciones"

    def __str__(self):
        return f"{self.usuario} - {self.mensaje[:40]}"