from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from citas.models import Cita
from citas.reglas import HORAS_MIN_CANCELACION
from notificaciones.models import Notificacion
from notificaciones.utils import notificar, usuario_de_cliente


class Command(BaseCommand):
    help = (
        "Avisa al cliente que su cita es mañana y que ya terminó el plazo "
        "para cancelarla sin penalización (24 h antes). Ejecutar cada hora."
    )

    MARCA = "plazo para cancelar"

    def handle(self, *args, **options):
        ahora = timezone.now()
        enviados = 0
        citas = Cita.objects.filter(
            estado__in=["Pendiente", "Confirmada"],
            fecha__range=(ahora.date(), ahora.date() + timedelta(days=2)),
        ).select_related("cliente", "barbero")
        for cita in citas:
            inicio = cita.inicio
            if inicio is None:
                continue
            horas = (inicio - ahora).total_seconds() / 3600
            # Ventana de aviso: entre 24 y 27 horas antes (queda 1-3 h para cancelar).
            if not (HORAS_MIN_CANCELACION <= horas <= HORAS_MIN_CANCELACION + 3):
                continue
            usuario = usuario_de_cliente(cita.cliente)
            if usuario is None:
                continue
            if Notificacion.objects.filter(usuario=usuario, cita=cita, mensaje__icontains=self.MARCA).exists():
                continue
            notificar(
                usuario,
                f"⏰ Tu cita es el {cita.fecha.strftime('%d/%m/%Y')} a las {cita.hora}. "
                f"El {self.MARCA} sin penalización termina pronto: "
                f"después ya no podrás cancelar y no asistir tendrá penalización.",
                cita=cita,
            )
            enviados += 1
        self.stdout.write(self.style.SUCCESS(f"Avisos enviados: {enviados}"))
