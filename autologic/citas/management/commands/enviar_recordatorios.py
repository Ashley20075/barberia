from datetime import datetime, timedelta

from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from twilio.rest import Client

from citas.models import Cita


class Command(BaseCommand):
    help = "Busca citas próximas y prepara los recordatorios de WhatsApp."

    def handle(self, *args, **options):

        # =====================================================
        # HORA ACTUAL DE COLOMBIA
        # =====================================================

        ahora = timezone.localtime()

        self.stdout.write(
            self.style.WARNING(
                f"\nHora actual: " f"{ahora.strftime('%d/%m/%Y %I:%M %p')}"
            )
        )

        self.stdout.write("\n🔎 Revisando citas próximas a una hora...\n")

        # =====================================================
        # BUSCAR CITAS DEL MISMO DÍA
        # =====================================================

        citas = Cita.objects.filter(
            fecha=ahora.date(),
            estado__in=["Pendiente", "Confirmada"],
            recordatorio_enviado=False,
        )

        citas_encontradas = []

        # =====================================================
        # REVISAR CADA CITA
        # =====================================================

        for cita in citas:

            try:
                hora_cita = datetime.strptime(
                    cita.hora, "%I:%M %p"
                ).time()

            except ValueError:
                self.stdout.write(
                    self.style.ERROR(
                        f"❌ No se pudo interpretar la hora "
                        f"de la cita {cita.id}: {cita.hora}"
                    )
                )
                continue

            # =================================================
            # FECHA + HORA DE LA CITA
            # =================================================

            fecha_hora_cita = datetime.combine(cita.fecha, hora_cita)

            fecha_hora_cita = timezone.make_aware(
                fecha_hora_cita, timezone.get_current_timezone()
            )

            # =================================================
            # CALCULAR MINUTOS FALTANTES
            # =================================================

            minutos_faltantes = (
                fecha_hora_cita - ahora
            ).total_seconds() / 60

            # =================================================
            # RECORDATORIO
            #
            # Se envía cuando:
            #
            # - Faltan 60 minutos o menos
            # - Todavía no ha pasado la hora de la cita
            #
            # Esto evita perder el recordatorio si el comando
            # se ejecuta unos minutos tarde.
            # =================================================

            if 0 < minutos_faltantes <= 60:

                citas_encontradas.append(cita)

                self.stdout.write(
                    self.style.SUCCESS("\n✅ CITA ENCONTRADA")
                )

                self.stdout.write(f"ID: {cita.id}")

                self.stdout.write(f"Cliente: {cita.cliente.nombre}")

                self.stdout.write(f"Teléfono: {cita.cliente.telefono}")

                self.stdout.write(f"Fecha: {cita.fecha}")

                self.stdout.write(f"Hora: {cita.hora}")

                self.stdout.write(f"Servicio: {cita.servicio.nombre}")

                self.stdout.write(
                    f"Barbero: "
                    f"{cita.barbero.nombre if cita.barbero else 'Por asignar'}"
                )

                self.stdout.write(f"Estado: {cita.estado}")

                self.stdout.write(
                    f"Faltan aproximadamente: "
                    f"{round(minutos_faltantes)} minutos"
                )

                # =================================================
                # CREAR MENSAJE
                # =================================================

                mensaje = (
                    f"🔔 Recordatorio de cita - BarberSpringfield\n\n"
                    f"Hola {cita.cliente.nombre}, te recordamos "
                    f"que tienes una cita programada para hoy.\n\n"
                    f"✂️ Servicio: {cita.servicio.nombre}\n"
                    f"💈 Barbero: "
                    f"{cita.barbero.nombre if cita.barbero else 'Por asignar'}\n"
                    f"🕐 Hora: {cita.hora}\n\n"
                    f"¡Te esperamos en BarberSpringfield! 💈"
                )

                self.stdout.write(
                    self.style.SUCCESS(
                        f"\n📱 MENSAJE PREPARADO:\n" f"{mensaje}\n"
                    )
                )

                # =================================================
                # ENVIAR RECORDATORIO POR WHATSAPP
                # =================================================

                try:
                    telefono = cita.cliente.telefono

                    if not telefono:
                        self.stdout.write(
                            self.style.ERROR(
                                f"❌ El cliente {cita.cliente.nombre} "
                                f"no tiene número de teléfono."
                            )
                        )
                        continue

                    # Convertir número colombiano a formato internacional
                    if telefono.startswith("3"):
                        telefono = "+57" + telefono

                    client = Client(
                        settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN
                    )

                    mensaje_twilio = client.messages.create(
                        from_=settings.TWILIO_WHATSAPP_FROM,
                        content_sid="HXfe5ab5f00277942d4d4200328b4d403c",
                        to=f"whatsapp:{telefono}",
                    )

                    self.stdout.write(
                        self.style.SUCCESS(
                            f"📱 WhatsApp enviado correctamente."
                        )
                    )

                    self.stdout.write(f"SID: {mensaje_twilio.sid}")

                    self.stdout.write(f"Estado: {mensaje_twilio.status}")

                    # =================================================
                    # MARCAR COMO ENVIADO SOLO SI TWILIO ACEPTÓ EL MENSAJE
                    # =================================================

                    cita.recordatorio_enviado = True

                    cita.save(update_fields=["recordatorio_enviado"])

                    self.stdout.write(
                        self.style.SUCCESS(
                            "✅ Recordatorio marcado como enviado."
                        )
                    )

                except Exception as e:

                    self.stdout.write(
                        self.style.ERROR(f"❌ Error enviando WhatsApp: {e}")
                    )

        # =====================================================
        # RESULTADO FINAL
        # =====================================================

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