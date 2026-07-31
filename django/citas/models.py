from datetime import datetime, timedelta
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

    estado = models.CharField(
        max_length=20,
        choices=ESTADOS,
        default="Pendiente"
    )

    class Meta:
        ordering = ["fecha", "hora"]
        constraints = [
            models.UniqueConstraint(
                fields=["barbero", "fecha", "hora"],
                name="cita_unica_por_barbero"
            )
        ]

    def clean(self):

        # Validar que un cliente no tenga más de una cita el mismo día
        cita_cliente = Cita.objects.filter(
            cliente=self.cliente,
            fecha=self.fecha
        ).exclude(
            pk=self.pk
        ).exclude(
            estado="Cancelada"
        )

        if cita_cliente.exists():
            raise ValidationError(
                "El cliente ya tiene una cita registrada para esta fecha."
            )

        # Validaciones del barbero
        if self.barbero:

            if not self.barbero.es_dia_laboral(self.fecha):
                raise ValidationError(
                    f"El barbero {self.barbero.nombre} no trabaja en esta fecha."
                )

            if self.barbero.es_dia_descanso(self.fecha):
                raise ValidationError(
                    f"El barbero {self.barbero.nombre} tiene descanso en esta fecha."
                )

            # Convertir hora actual a datetime
            inicio_nueva = datetime.strptime(
                self.hora,
                "%I:%M %p"
            )

            fin_nueva = inicio_nueva + timedelta(
                minutes=self.servicio.duracion
            )

            citas_existentes = Cita.objects.filter(
                barbero=self.barbero,
                fecha=self.fecha
            ).exclude(
                pk=self.pk
            ).exclude(
                estado="Cancelada"
            )

            for cita in citas_existentes:

                inicio_existente = datetime.strptime(
                    cita.hora,
                    "%I:%M %p"
                )

                fin_existente = inicio_existente + timedelta(
                    minutes=cita.servicio.duracion
                )

                # Validar cruce de horarios
                if (
                    inicio_nueva < fin_existente
                    and
                    fin_nueva > inicio_existente
                ):
                    raise ValidationError(
                        f"El horario seleccionado se cruza con otra cita del barbero "
                        f"({inicio_existente.strftime('%I:%M %p')} - "
                        f"{fin_existente.strftime('%I:%M %p')})."
                    )

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