from datetime import datetime, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.conf import settings
from twilio.rest import Client

from citas.models import Cita


class Command(BaseCommand):
    help = "Busca citas próximas y prepara los recordatorios de WhatsApp."

    def handle(self, *args, **options):

        client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

        ahora = timezone.localtime()

        limite_inferior = ahora + timedelta(minutes=55)
        limite_superior = ahora + timedelta(minutes=65)

        self.stdout.write(
            self.style.WARNING(
                f"\nHora actual: {ahora.strftime('%d/%m/%Y %I:%M %p')}"
            )
        )

        self.stdout.write(
            f"Buscando citas entre "
            f"{limite_inferior.strftime('%I:%M %p')} y "
            f"{limite_superior.strftime('%I:%M %p')}...\n"
        )

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
                        f"❌ No se pudo interpretar la hora de la cita {cita.id}: "
                        f"{cita.hora}"
                    )
                )
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
                    f"Estado: {cita.estado}"
                )

                self.stdout.write(
                    f"Faltan aproximadamente: "
                    f"{round(minutos_faltantes)} minutos"
                )

                # Crear el mensaje del recordatorio
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

                # Envío real del mensaje vía Twilio WhatsApp
                try:
                    telefono = cita.cliente.telefono.strip()

                    if not telefono.startswith('+'):
                        telefono = '+57' + telefono

                    mensaje_whatsapp = client.messages.create(
                        from_=settings.TWILIO_WHATSAPP_FROM,
                        body=mensaje,
                        to=f'whatsapp:{telefono}'
                    )

                    cita.recordatorio_enviado = True
                    cita.save(update_fields=['recordatorio_enviado'])

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"\n✅ WhatsApp enviado correctamente"
                        )
                    )

                    self.stdout.write(
                        f"📱 Destinatario: {telefono}"
                    )

                    self.stdout.write(
                        f"🆔 SID del mensaje: {mensaje_whatsapp.sid}\n"
                    )

                except Exception as e:
                    self.stdout.write(
                        self.style.ERROR(
                            f"\n❌ Error enviando WhatsApp: {str(e)}\n"
                        )
                    )

        if not citas_encontradas:

            self.stdout.write(
                self.style.WARNING(
                    "\n⚠️ No hay citas que necesiten recordatorio en este momento."
                )
            )

        else:

            self.stdout.write(
                self.style.SUCCESS(
                    f"\n🎯 Total de citas encontradas: "
                    f"{len(citas_encontradas)}"
                )
            )