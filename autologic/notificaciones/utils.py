from django.contrib.auth.models import User

from .models import Notificacion


def notificar(usuario, mensaje, cita=None):
    """Crea una notificación para `usuario`. No hace nada si usuario es None."""
    if usuario is None:
        return
    Notificacion.objects.create(usuario=usuario, mensaje=mensaje, cita=cita)


def usuario_de_barbero(barbero):
    """Devuelve el User que corresponde a un Barbero, si existe."""
    if not barbero:
        return None
    return User.objects.filter(email=barbero.email, is_active=True).first()


def usuario_de_cliente(cliente):
    """Devuelve el User dueño de un Cliente, si existe."""
    if not cliente:
        return None
    return getattr(cliente, "user", None)


def notificar_administradores(mensaje, cita=None):
    """Notifica a todas las cuentas administradoras (superusuarios)."""
    for administrador in User.objects.filter(is_superuser=True, is_active=True):
        notificar(administrador, mensaje, cita=cita)
