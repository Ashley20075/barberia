from datetime import datetime, timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from barberos.models import Barbero
from clientes.models import Cliente


class SuscriptorNewsletter(models.Model):
    """
    Antes, el formulario "Tu correo" del pie de página no guardaba
    nada: el botón no tenía ni un onclick, el input no tenía name, y
    no existía ninguna vista que lo recibiera.
    """
    email = models.EmailField(unique=True)
    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creado"]
        verbose_name = "Suscriptor al newsletter"
        verbose_name_plural = "Suscriptores al newsletter"

    def __str__(self):
        return self.email


class Servicio(models.Model):
    nombre = models.CharField(max_length=100)

    descripcion = models.TextField()

    precio = models.PositiveIntegerField()

    duracion = models.PositiveIntegerField(
        help_text="Duración en minutos"
    )

    imagen = models.URLField(
        blank=True,
        default="",
        help_text="URL de la imagen del estilo o corte"
    )

    def __str__(self):
        return self.nombre


class Cita(models.Model):
    ESTADOS = [
        ("Pendiente", "Pendiente"),
        ("Confirmada", "Confirmada"),
        ("Cancelada", "Cancelada"),
        ("Finalizada", "Finalizada"),
        ("NoAsistio", "No asistió"),
    ]

    FALTAS = [
        ("cliente", "El cliente no asistió"),
        ("barbero", "El barbero no asistió"),
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

    historial_archivado = models.BooleanField(default=False)

    # ==========================================
    # ANÁLISIS REALIZADO POR AUTOAI
    # ==========================================
    analisis_ia = models.JSONField(
        default=dict,
        blank=True
    )

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Pendiente"
    )

    # Solo se llena cuando estado == "NoAsistio": quién faltó a la cita.
    falta_de = models.CharField(
        max_length=10,
        choices=FALTAS,
        blank=True,
        default=""
    )

    # Corte gratis canjeado (programa de fidelidad: cada 10 cortes, el siguiente es gratis)
    corte_gratis = models.BooleanField(default=False)

    @property
    def inicio(self):
        """Fecha y hora de inicio de la cita (aware), o None si la hora es inválida."""
        from django.utils import timezone
        try:
            hora = datetime.strptime(self.hora, "%I:%M %p").time()
        except (TypeError, ValueError):
            return None
        return timezone.make_aware(datetime.combine(self.fecha, hora))

    @property
    def precio_cobrado(self):
        return 0 if self.corte_gratis else self.servicio.precio

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


class Resena(models.Model):
    """Calificación opcional que deja el cliente al terminar su cita."""

    cita = models.OneToOneField(
        Cita,
        on_delete=models.CASCADE,
        related_name="resena"
    )

    puntuacion = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )

    comentario = models.TextField(
        max_length=500,
        blank=True,
        default=""
    )

    creada = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-creada"]
        verbose_name = "Reseña"
        verbose_name_plural = "Reseñas"

    def __str__(self):
        return f"{self.cita.cliente.nombre}: {self.puntuacion}/5"
