"""
Cálculos del reporte de "cierre de caja".

Esta lógica vive separada de administracion/views.py a propósito: así
tanto la vista HTML (cierre_caja) como la vista que genera el PDF
(cierre_caja_pdf) reusan exactamente el mismo cálculo, en vez de tener
la misma cuenta de ingresos/citas escrita dos veces en dos vistas.

El reporte admite un rango de fecha-hora: se filtra por fecha_inicio/
fecha_fin (ambas inclusive) y, opcionalmente, por una franja horaria
(hora_inicio/hora_fin) que se aplica dentro de cada día del rango.
"""

from datetime import datetime

from citas.models import Cita


def calcular_cierre_caja(fecha_inicio, fecha_fin, hora_inicio=None, hora_fin=None):
    """
    Devuelve el resumen del rango [fecha_inicio, fecha_fin]: servicios
    finalizados (con sus ingresos), citas canceladas y citas que
    quedaron pendientes/confirmadas sin resolver en ese período.

    Si se indican hora_inicio y hora_fin, el rango horario se aplica
    dentro de cada día del período.

    OJO: `hora_inicio`/`hora_fin` llegan del <input type="time"> del
    filtro en formato 24 horas ("14:30"), pero `Cita.hora` se guarda
    como texto en formato 12 horas con AM/PM ("02:30 PM") -son cosas
    que agenda_cita crea con strptime(..., "%I:%M %p"). Comparar esas
    dos cadenas de texto directamente (hora__gte=hora_inicio) nunca
    coincide con el orden real del día: por eso el filtro de horas del
    cierre de caja no traía resultados. Se convierte todo a objetos
    `time` antes de comparar.
    """

    citas_del_rango = (
        Cita.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        .select_related("cliente", "servicio", "barbero")
        .order_by("fecha", "hora")
    )

    rango_horario = None
    if hora_inicio and hora_fin:
        try:
            rango_horario = (
                datetime.strptime(hora_inicio, "%H:%M").time(),
                datetime.strptime(hora_fin, "%H:%M").time(),
            )
        except ValueError:
            rango_horario = None

    if rango_horario:
        desde, hasta = rango_horario
        citas_filtradas = []
        for cita in citas_del_rango:
            try:
                hora_cita = datetime.strptime(cita.hora, "%I:%M %p").time()
            except (ValueError, TypeError):
                continue
            if desde <= hora_cita <= hasta:
                citas_filtradas.append(cita)
        citas_del_rango = citas_filtradas

    finalizadas = [c for c in citas_del_rango if c.estado == "Finalizada"]
    canceladas = [c for c in citas_del_rango if c.estado == "Cancelada"]
    pendientes = [c for c in citas_del_rango if c.estado in ("Pendiente", "Confirmada")]

    total_ingresos = sum(cita.servicio.precio for cita in finalizadas)

    por_barbero = {}
    for cita in finalizadas:
        nombre = cita.barbero.nombre if cita.barbero else "Sin asignar"
        info = por_barbero.setdefault(nombre, {"cantidad": 0, "ingresos": 0})
        info["cantidad"] += 1
        info["ingresos"] += cita.servicio.precio

    return {
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
        "hora_inicio": hora_inicio,
        "hora_fin": hora_fin,
        "es_rango": fecha_inicio != fecha_fin,
        "finalizadas": finalizadas,
        "canceladas": canceladas,
        "pendientes": pendientes,
        "total_finalizadas": len(finalizadas),
        "total_canceladas": len(canceladas),
        "total_pendientes": len(pendientes),
        "total_ingresos": total_ingresos,
        "por_barbero": por_barbero,
    }