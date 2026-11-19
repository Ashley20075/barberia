"""Programa de fidelidad: cada 10 cortes finalizados se gana un CUPÓN de corte gratis."""
from django.db import transaction

from notificaciones.utils import (
    notificar, notificar_administradores, usuario_de_barbero, usuario_de_cliente,
)

CORTES_PARA_RECOMPENSA = 10


def aplicar_cupon(cita):
    """
    Usa un cupón al AGENDAR: descuenta una recompensa, marca la cita como
    corte gratis (cobro $0) y avisa a cliente, barbero y administradores.
    Devuelve True si se aplicó.
    """
    from citas.models import Cita
    from clientes.models import Cliente

    with transaction.atomic():
        cliente = Cliente.objects.select_for_update().get(pk=cita.cliente_id)
        if cliente.recompensas_disponibles <= 0 or cita.corte_gratis:
            return False
        cliente.recompensas_disponibles -= 1
        cliente.save(update_fields=['recompensas_disponibles'])
        # update() evita el full_clean de Cita.save()
        Cita.objects.filter(pk=cita.pk).update(corte_gratis=True)
        cita.corte_gratis = True
        notificar(usuario_de_cliente(cliente),
                  '🎟️ Usaste tu cupón de corte gratis en tu nueva cita. Se cobrará $0.', cita=cita)
        notificar_administradores(
            f'🎟️ {cliente.nombre} agendó con cupón de corte gratis (cobro $0).', cita=cita)
    return True


def devolver_cupon(cita):
    """Si una cita con cupón se cancela, el cupón vuelve al cliente."""
    from citas.models import Cita
    from clientes.models import Cliente

    if not cita.corte_gratis:
        return False
    with transaction.atomic():
        cliente = Cliente.objects.select_for_update().get(pk=cita.cliente_id)
        cliente.recompensas_disponibles += 1
        cliente.save(update_fields=['recompensas_disponibles'])
        Cita.objects.filter(pk=cita.pk).update(corte_gratis=False)
        cita.corte_gratis = False
        notificar(usuario_de_cliente(cliente),
                  '🎟️ Tu cita con cupón fue cancelada: tu cupón de corte gratis volvió a estar disponible.',
                  cita=cita)
    return True


def procesar_finalizacion(cita):
    """
    Llamar UNA vez cuando la cita pasa a 'Finalizada'.
    - Cita con cupón: no suma al siguiente ciclo ('cupon').
    - Cita normal: suma 1; al llegar a 10 se otorga un cupón y el contador
      se reinicia ('ganada'); si no, 'normal'.
    """
    from clientes.models import Cliente

    if cita.corte_gratis:
        return 'cupon'

    with transaction.atomic():
        cliente = Cliente.objects.select_for_update().get(pk=cita.cliente_id)
        cliente.cortes_completados += 1
        cliente.cortes_para_recompensa += 1
        resultado = 'normal'
        if cliente.cortes_para_recompensa >= CORTES_PARA_RECOMPENSA:
            cliente.cortes_para_recompensa = 0
            cliente.recompensas_disponibles += 1
            resultado = 'ganada'
        cliente.save(update_fields=['cortes_completados', 'cortes_para_recompensa', 'recompensas_disponibles'])

        if resultado == 'ganada':
            barbero_user = usuario_de_barbero(cita.barbero)
            notificar(usuario_de_cliente(cliente),
                      '🎟️ ¡Felicitaciones! Completaste 10 cortes: ganaste un cupón de corte gratis. '
                      'Úsalo al agendar tu próxima cita.', cita=cita)
            notificar(barbero_user, f'🎟️ {cliente.nombre} ganó un cupón de corte gratis.', cita=cita)
            notificar_administradores(f'🎟️ {cliente.nombre} ganó un cupón de corte gratis.', cita=cita)
        return resultado
