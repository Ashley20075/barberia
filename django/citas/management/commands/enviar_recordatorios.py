from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from citas.models import Cita


class Command(BaseCommand):
    help = "Busca citas próximas y prepara los recordatorios de WhatsApp."

    def handle(self, *args, **options):
        ahora = timezone.localtime()

        hora_inicio = ahora.replace(
            hour=8,
            minute=0,
            second=0,
            microsecond=0
        )

        hora_fin = ahora.replace(
            hour=17,
            minute=15,
            second=0,
            microsecond=0
        )

        self.stdout.write(
            self.style.WARNING(
                f"\nHora actual: {ahora.strftime('%d/%m/%Y %I:%M %p')}"
            )
        )

        # Verificar horario de atención
        if ahora < hora_inicio or ahora > hora_fin:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️ Fuera del horario de atención de BarberSpringfield."
                )
            )

            self.stdout.write(
                "Las citas están disponibles entre 08:00 AM y 05:15 PM."
            )

            return

        limite_inferior = ahora + timedelta(minutes=55)
        limite_superior = ahora + timedelta(minutes=65)

        self.stdout.write(
            f"Buscando citas entre "
            f"{limite_inferior.strftime('%I:%M %p')} y "
            f"{limite_superior.strftime('%I:%M %p')}...\n"
        )

        # Solo procesamos citas dentro del horario de atención
        citas = Cita.objects.filter(
            fecha=limite_inferior.date(),
            estado__in=["Pendiente", "Confirmada"],
            recordatorio_enviado=False
        )

        citas_encontradas = []

        for cita in citas:
            try:
                hora_cita = datetime.strptime(
                    cita.hora,
                    "%I:%M %p"
                ).time()

            except ValueError:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ No se pudo interpretar la hora de la cita "
                        f"{cita.id}: {cita.hora}"
                    )
                )
                continue

            # Horario permitido para las citas:
            # 08:00 AM hasta 05:15 PM
            if hora_cita < datetime.strptime("08:00 AM", "%I:%M %p").time():
                continue

            if hora_cita > datetime.strptime("05:15 PM", "%I:%M %p").time():
                continue

            fecha_hora_cita = datetime.combine(
                cita.fecha,
                hora_cita
            )

            fecha_hora_cita = timezone.make_aware(
                fecha_hora_cita,
                timezone.get_current_timezone()
            )

            minutos_faltantes = (
                fecha_hora_cita - ahora
            ).total_seconds() / 60

            # Cita aproximadamente una hora después
            if 55 <= minutos_faltantes <= 65:
                citas_encontradas.append(cita)

                self.stdout.write(
                    self.style.SUCCESS(
                        "\n✅ CITA ENCONTRADA"
                    )
                )

                self.stdout.write(
                    f"ID: {cita.id}"
                )

                self.stdout.write(
                    f"Cliente: {cita.cliente.nombre}"
                )

                self.stdout.write(
                    f"Teléfono: {cita.cliente.telefono}"
                )

                self.stdout.write(
                    f"Fecha: {cita.fecha}"
                )

                self.stdout.write(
                    f"Hora: {cita.hora}"
                )

                self.stdout.write(
                    f"Servicio: {cita.servicio.nombre}"
                )

                self.stdout.write(
                    f"Barbero: "
                    f"{cita.barbero.nombre if cita.barbero else 'Por asignar'}"
                )

                self.stdout.write(
                    f"Estado: {cita.estado}"
                )

                self.stdout.write(
                    f"Faltan aproximadamente: "
                    f"{round(minutos_faltantes)} minutos"
                )

                # Mensaje que posteriormente enviaremos por WhatsApp
                mensaje = (
                    f"🔔 Recordatorio de cita - BarberSpringfield\n\n"
                    f"Hola {cita.cliente.nombre}, te recordamos que tienes "
                    f"una cita programada para hoy.\n\n"
                    f"✂️ Servicio: {cita.servicio.nombre}\n"
                    f"💈 Barbero: "
                    f"{cita.barbero.nombre if cita.barbero else 'Por asignar'}\n"
                    f"🕐 Hora: {cita.hora}\n\n"
                    f"¡Te esperamos en BarberSpringfield! 💈"
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n📱 MENSAJE PREPARADO:\n{mensaje}\n"
                    )
                )

                # Por ahora solamente marcamos el recordatorio
                # como procesado. WhatsApp se conectará después.
                cita.recordatorio_enviado = True
                cita.save(update_fields=["recordatorio_enviado"])

                self.stdout.write(
                    self.style.SUCCESS(
                        "✅ Recordatorio marcado como enviado."
                    )
                )

        if not citas_encontradas:
            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️ No hay citas que necesiten "
                    "recordatorio en este momento."
                )
            )

        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎯 Total de citas encontradas: "
                    f"{len(citas_encontradas)}"
                )
            )