from datetime import datetime, timedelta

from django.utils import timezone

from .models import Cita


def buscar_citas_para_recordatorio():
    ahora = timezone.localtime()

    limite_inferior = ahora + timedelta(minutes=59)
    limite_superior = ahora + timedelta(minutes=61)

    citas = Cita.objects.filter(
        estado__in=["Pendiente", "Confirmada"],
        recordatorio_enviado=False,
        fecha=ahora.date(),
    )

    citas_recordatorio = []

    for cita in citas:

        try:
            hora_cita = datetime.strptime(
                cita.hora,
                "%I:%M %p"
            ).time()

        except ValueError:
            continue

        fecha_hora_cita = datetime.combine(
            cita.fecha,
            hora_cita
        )

        fecha_hora_cita = timezone.make_aware(
            fecha_hora_cita,
            timezone.get_current_timezone()
        )

        diferencia = fecha_hora_cita - ahora

        if limite_inferior <= diferencia <= limite_superior:
            citas_recordatorio.append(cita)

    return citas_recordatorio

def probar_recordatorios():

    citas = buscar_citas_para_recordatorio()

    for cita in citas:
        print("================================")
        print("📱 RECORDATORIO ENCONTRADO")
        print("Cliente:", cita.cliente.nombre)
        print("Teléfono:", cita.cliente.telefono)
        print("Servicio:", cita.servicio.nombre)
        print("Barbero:", cita.barbero.nombre if cita.barbero else "Sin asignar")
        print("Fecha:", cita.fecha)
        print("Hora:", cita.hora)
        print("================================")

    return citas