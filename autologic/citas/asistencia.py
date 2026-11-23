"""Inasistencias (cliente o barbero) y sus consecuencias."""
from datetime import timedelta

from django.db import transaction
from django.utils import timezone

from notificaciones.utils import (
    notificar, notificar_administradores, usuario_de_barbero, usuario_de_cliente,
)

from .reglas import dias_de_penalizacion, puede_marcar_inasistencia


class InasistenciaInvalida(Exception):
    """La cita no se puede marcar como 'no asistió'."""


def _devolver_productos(cita, usuario):
    """Los productos reservados al agendar no se usaron: vuelven al inventario."""
    from inventario.models import Producto
    from inventario.utils import registrar_movimiento

    if not cita.productos or cita.productos == "Ninguno":
        return
    for nombre in cita.productos.split(","):
        producto = Producto.objects.filter(nombre=nombre.strip()).first()
        if producto is None:
            continue
        try:
            registrar_movimiento(
                producto=producto, tipo="ENTRADA", cantidad=1, usuario=usuario,
                nota=f"Devolución por inasistencia en cita de {cita.cliente.nombre}",
                validar_maximo=False,
            )
        except Exception:
            pass


def marcar_no_asistio(cita, falta_de, por=None):
    """
    Marca la cita como 'No asistió'.

    falta_de == "cliente": suma una falta al cliente y aplica la penalización
        (1.ª advertencia, 2.ª 7 días sin agendar, 3.ª+ 15 días). Si la cita
        usaba un cupón, el cupón se pierde.
    falta_de == "barbero": suma una falta al barbero, avisa al administrador y
        le regala al cliente un cupón de corte gratis como compensación.
    """
    from barberos.models import Barbero
    from clientes.models import Cliente

    if falta_de not in ("cliente", "barbero"):
        raise InasistenciaInvalida("Indica quién no asistió.")
    if cita.estado not in ("Pendiente", "Confirmada"):
        raise InasistenciaInvalida("Solo se puede marcar una cita pendiente o confirmada.")
    if not puede_marcar_inasistencia(cita):
        raise InasistenciaInvalida(
            "Todavía no se puede marcar: debe haber pasado la hora de la cita."
        )

    fecha = cita.fecha.strftime("%d/%m/%Y")
    mensaje_cita = f"{fecha} a las {cita.hora}"

    with transaction.atomic():
        cita.estado = "NoAsistio"
        cita.falta_de = falta_de
        cita.save()
        _devolver_productos(cita, por)

        cliente = Cliente.objects.select_for_update().get(pk=cita.cliente_id)
        usuario_cli = usuario_de_cliente(cliente)
        usuario_bar = usuario_de_barbero(cita.barbero)

        if falta_de == "cliente":
            cliente.inasistencias += 1
            dias = dias_de_penalizacion(cliente.inasistencias)
            if dias:
                cliente.penalizado_hasta = timezone.localdate() + timedelta(days=dias)
            cliente.save(update_fields=["inasistencias", "penalizado_hasta"])

            if dias:
                texto = (
                    f"⚠️ No asististe a tu cita del {mensaje_cita}. Es tu falta n.º "
                    f"{cliente.inasistencias}: no podrás agendar nuevas citas hasta el "
                    f"{cliente.penalizado_hasta.strftime('%d/%m/%Y')}."
                )
            else:
                texto = (
                    f"⚠️ No asististe a tu cita del {mensaje_cita}. Esta es una advertencia: "
                    "si vuelves a faltar no podrás agendar citas durante 7 días."
                )
            if cita.corte_gratis:
                texto += " El cupón de corte gratis de esa cita se perdió."
            notificar(usuario_cli, texto, cita=cita)
            notificar(usuario_bar, f"Registraste que {cliente.nombre} no asistió a la cita del {mensaje_cita}.", cita=cita)
            notificar_administradores(
                f"⚠️ {cliente.nombre} no asistió a su cita del {mensaje_cita} "
                f"(falta n.º {cliente.inasistencias}).", cita=cita)
        else:
            if cita.barbero_id:
                barbero = Barbero.objects.select_for_update().get(pk=cita.barbero_id)
                barbero.inasistencias += 1
                barbero.save(update_fields=["inasistencias"])
            cliente.recompensas_disponibles += 1
            cliente.save(update_fields=["recompensas_disponibles"])
            nombre_b = cita.barbero.nombre if cita.barbero else "el barbero"
            notificar(
                usuario_cli,
                f"⚠️ {nombre_b} no asistió a tu cita del {mensaje_cita}. Lamentamos el inconveniente: "
                "te regalamos un 🎟️ cupón de corte gratis, úsalo al agendar tu próxima cita.",
                cita=cita)
            notificar(usuario_bar, f"Se registró que no asististe a la cita de {cliente.nombre} del {mensaje_cita}.", cita=cita)
            notificar_administradores(
                f"⚠️ {nombre_b} no asistió a la cita de {cliente.nombre} del {mensaje_cita}. "
                "Se compensó al cliente con un cupón de corte gratis.", cita=cita)
    return cita
