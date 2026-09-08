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

from citas.models import Cita


def calcular_cierre_caja(fecha_inicio, fecha_fin, hora_inicio=None, hora_fin=None):
    """
    Devuelve el resumen del rango [fecha_inicio, fecha_fin]: servicios
    finalizados (con sus ingresos), citas canceladas y citas que
    quedaron pendientes/confirmadas sin resolver en ese período.

    Si se indican hora_inicio y hora_fin (strings "HH:MM"), el rango
    horario se aplica dentro de cada día del período. `hora` se guarda
    como texto con formato "HH:MM", por lo que la comparación de
    strings coincide con el orden cronológico.
    """

    citas_del_rango = (
        Cita.objects.filter(fecha__range=[fecha_inicio, fecha_fin])
        .select_related("cliente", "servicio", "barbero")
        .order_by("fecha", "hora")
    )

    if hora_inicio and hora_fin:
        citas_del_rango = citas_del_rango.filter(hora__gte=hora_inicio, hora__lte=hora_fin)

    finalizadas = citas_del_rango.filter(estado="Finalizada")
    canceladas = citas_del_rango.filter(estado="Cancelada")
    pendientes = citas_del_rango.filter(estado__in=["Pendiente", "Confirmada"])

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
        "total_finalizadas": finalizadas.count(),
        "total_canceladas": canceladas.count(),
        "total_pendientes": pendientes.count(),
        "total_ingresos": total_ingresos,
        "por_barbero": por_barbero,
    }