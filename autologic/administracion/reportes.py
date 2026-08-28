"""
Cálculos del reporte de "cierre de caja diario".

Esta lógica vive separada de administracion/views.py a propósito: así
tanto la vista HTML (cierre_caja) como la vista que genera el PDF
(cierre_caja_pdf) reusan exactamente el mismo cálculo, en vez de tener
la misma cuenta de ingresos/citas escrita dos veces en dos vistas.
"""

from citas.models import Cita


def calcular_cierre_caja(fecha):
    """
    Devuelve el resumen de un día: servicios finalizados (con sus
    ingresos), citas canceladas y citas que quedaron pendientes/
    confirmadas sin resolver ese día.
    """

    citas_del_dia = (
        Cita.objects.filter(fecha=fecha)
        .select_related("cliente", "servicio", "barbero")
        .order_by("hora")
    )

    finalizadas = citas_del_dia.filter(estado="Finalizada")
    canceladas = citas_del_dia.filter(estado="Cancelada")
    pendientes = citas_del_dia.filter(estado__in=["Pendiente", "Confirmada"])

    total_ingresos = sum(cita.servicio.precio for cita in finalizadas)

    por_barbero = {}
    for cita in finalizadas:
        nombre = cita.barbero.nombre if cita.barbero else "Sin asignar"
        info = por_barbero.setdefault(nombre, {"cantidad": 0, "ingresos": 0})
        info["cantidad"] += 1
        info["ingresos"] += cita.servicio.precio

    return {
        "fecha": fecha,
        "finalizadas": finalizadas,
        "canceladas": canceladas,
        "pendientes": pendientes,
        "total_finalizadas": finalizadas.count(),
        "total_canceladas": canceladas.count(),
        "total_pendientes": pendientes.count(),
        "total_ingresos": total_ingresos,
        "por_barbero": por_barbero,
    }
