"""
El numero de notificaciones sin leer se calculaba a mano dentro de un
par de vistas (el panel del cliente, el del barbero, el del admin).
Cualquier otra pagina que usara la misma navbar -sobre todo "Editar
perfil"- nunca recibia esa variable, asi que la campanita se quedaba
sin su numero en cuanto se salia del panel principal, aunque las
notificaciones siguieran sin leerse.

Este context processor calcula el conteo UNA vez, en un solo lugar,
para cualquier pagina que lo necesite: asi no depende de que cada
vista se acuerde de agregarlo a mano.
"""


def notificaciones_no_leidas(request):
    if not request.user.is_authenticated:
        return {}

    return {
        "notificaciones_no_leidas":
            request.user.notificaciones.filter(leida=False).count()
    }
