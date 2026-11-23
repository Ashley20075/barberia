from django import template

register = template.Library()

# (clave, etiqueta, icono, palabras clave) — el orden importa.
CATEGORIAS = [
    ('falta', 'Inasistencia', 'bi-person-x', ('no asist', 'falta n.')),
    ('resena', 'Calificación', 'bi-star-fill', ('calificó', 'calificación')),
    ('cupon', 'Cupón', 'bi-ticket-perforated', ('corte gratis', 'cupón', 'cupon', 'canje')),
    ('espera', 'Lista de espera', 'bi-hourglass-split', ('lo estabas siguiendo', 'lista de espera')),
    ('rechazo', 'Cita cancelada', 'bi-x-octagon', ('rechaz', 'cancelad')),
    ('liberado', 'Turno liberado', 'bi-unlock', ('quedó libre', 'quedó disponible', 'desocup')),
    ('nueva', 'Nueva cita', 'bi-calendar-plus', ('nueva cita',)),
    ('confirmada', 'Cita confirmada', 'bi-calendar-check', ('confirmad',)),
]


@register.filter
def notif_info(mensaje):
    texto = (mensaje or '').lower()
    for clave, etiqueta, icono, palabras in CATEGORIAS:
        if any(p in texto for p in palabras):
            return {'clave': clave, 'etiqueta': etiqueta, 'icono': icono}
    return {'clave': 'info', 'etiqueta': 'Aviso', 'icono': 'bi-bell'}
