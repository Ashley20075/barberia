"""
Utilidades del módulo de inventario.

IMPORTANTE: cualquier parte del proyecto que modifique `Producto.stock_actual`
(citas, panel de barberos, panel de administración, etc.) debe hacerlo a
través de `registrar_movimiento()` en lugar de tocar el campo directamente.

Antes, varias vistas (clientes.views, barberos.views, administracion.views)
sumaban/restaban stock con `producto.stock_actual -= 1` + `producto.save()`
sin crear el `MovimientoInventario` correspondiente. Por eso esas entradas y
salidas cambiaban el stock pero NUNCA aparecían en el historial de
movimientos ni en el dashboard de inventario. Esta función centraliza la
lógica para que todo movimiento quede registrado.
"""
from django.db import transaction


def registrar_movimiento(producto, tipo, cantidad, usuario=None,
                         proveedor=None, nota=None):
    """
    Aplica un movimiento de stock sobre `producto` y deja constancia de él
    en `MovimientoInventario`.

    tipo: 'ENTRADA', 'SALIDA' o 'AJUSTE'
    cantidad:
        - ENTRADA/SALIDA: cantidad a sumar/restar (debe ser > 0)
        - AJUSTE: nuevo valor absoluto de stock

    Devuelve la instancia de MovimientoInventario creada.
    Lanza ValueError si la operación no es válida (p. ej. una salida mayor
    al stock disponible).
    """
    from .models import MovimientoInventario  # import local para evitar ciclos

    cantidad = int(cantidad)
    stock_anterior = producto.stock_actual

    if tipo == 'ENTRADA':
        if cantidad <= 0:
            raise ValueError('La cantidad de entrada debe ser mayor a 0.')
        stock_nuevo = stock_anterior + cantidad

    elif tipo == 'SALIDA':
        if cantidad <= 0:
            raise ValueError('La cantidad de salida debe ser mayor a 0.')
        if cantidad > stock_anterior:
            raise ValueError(
                f'Stock insuficiente para "{producto.nombre}" '
                f'(disponible: {stock_anterior}, solicitado: {cantidad}).'
            )
        stock_nuevo = stock_anterior - cantidad

    elif tipo == 'AJUSTE':
        stock_nuevo = cantidad

    else:
        raise ValueError(f'Tipo de movimiento inválido: {tipo}')

    with transaction.atomic():
        producto.stock_actual = stock_nuevo
        producto.save(update_fields=['stock_actual'])

        movimiento = MovimientoInventario.objects.create(
            producto=producto,
            tipo=tipo,
            cantidad=cantidad,
            stock_anterior=stock_anterior,
            stock_nuevo=stock_nuevo,
            proveedor=proveedor,
            usuario=usuario,
            nota=nota,
        )

    return movimiento
