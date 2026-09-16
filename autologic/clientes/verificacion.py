"""
Verificación de que el correo de una cuenta nueva EXISTE de verdad.

Por qué hace falta algo más que validar el formato
--------------------------------------------------
`validate_email()` solo comprueba que el texto tenga forma de correo.
"asdasd@gmail.com" pasa esa validación perfectamente y no existe. La
única manera fiable de saber que una dirección existe y es de quien dice
serlo es mandarle un mensaje y pedir que abra un enlace: si el correo no
existe, nunca llega y la cuenta nunca se activa.

Cómo funciona aquí
------------------
1. Al registrarse, el usuario se crea con `is_active = False`.
2. Se le envía un enlace con un token firmado (no se guarda en base de
   datos: va firmado con la SECRET_KEY y caduca solo).
3. Al abrir el enlace, la cuenta se activa y ya puede iniciar sesión.
4. Mientras tanto, el login le avisa de que revise su correo.

El token usa `TimestampSigner`, así que caduca por sí mismo y no hace
falta ni modelo nuevo ni migración.
"""
from django.conf import settings
from django.core import signing
from django.core.mail import send_mail
from django.urls import reverse

# Sal propia para que este token no sirva para nada más.
SAL = 'confirmacion-correo-barberia'

# Un día para confirmar.
VALIDEZ_SEGUNDOS = 60 * 60 * 24


def generar_token(user):
    """Token firmado que identifica al usuario a confirmar."""
    return signing.dumps({'uid': user.pk}, salt=SAL)


def leer_token(token):
    """
    Devuelve el id de usuario del token, o None si el token es falso,
    fue manipulado o ya caducó.
    """
    try:
        datos = signing.loads(token, salt=SAL, max_age=VALIDEZ_SEGUNDOS)
    except signing.SignatureExpired:
        return None
    except signing.BadSignature:
        return None
    return datos.get('uid')


def enviar_correo_confirmacion(request, user):
    """
    Envía el enlace de confirmación. Devuelve True si el envío salió
    bien y False si falló (por ejemplo, si el dominio del correo no
    existe y el servidor lo rechaza en el acto).
    """
    token = generar_token(user)
    ruta = reverse('confirmar_correo', args=[token])
    enlace = request.build_absolute_uri(ruta)

    asunto = 'Confirma tu correo - Barber Springfield'

    cuerpo = (
        f'Hola {user.first_name or user.username}:\n\n'
        f'Para terminar de crear tu cuenta en Barber Springfield, abre '
        f'este enlace:\n\n'
        f'{enlace}\n\n'
        f'El enlace caduca en 24 horas. Si no fuiste tú quien se '
        f'registró, simplemente ignora este mensaje.\n'
    )

    try:
        enviados = send_mail(
            asunto,
            cuerpo,
            getattr(settings, 'DEFAULT_FROM_EMAIL', None),
            [user.email],
            fail_silently=False,
        )
        return enviados > 0
    except Exception:
        # Un correo inexistente en un dominio que sí existe normalmente
        # se rechaza más tarde (rebote), no aquí; pero un dominio
        # inventado sí suele fallar en este punto.
        return False
