"""
Todas las vistas relacionadas con la autenticación/autorización de Google
viven aquí. Hay DOS flujos que comparten el mismo callback:

1) "conectar" -> el usuario YA tiene sesión iniciada (admin o barbero) y
   solo quiere anclar su Google Calendar. Botón "Conectar Google Calendar"
   en los paneles.

2) "login" -> el usuario NO tiene sesión iniciada. Con un solo clic en
   "Continuar con Google" se busca o se crea su cuenta automáticamente
   Y se conecta su calendario, sin pasos separados. Botón en login.html
   y registro.html.

Ambos flujos reusan `oauth2callback`, y se diferencian con la clave de
sesión `SESSION_ACCION_KEY` que se guarda antes de mandar al usuario a
Google. Así solo hace falta UN redirect URI configurado en Google Cloud
Console, en vez de uno por cada flujo.
"""

from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import transaction
from django.shortcuts import redirect

from google_auth_oauthlib.flow import Flow
from googleapiclient.discovery import build

from barberos.models import Barbero
from clientes.models import Cliente

from .models import CuentaGoogle

SESSION_STATE_KEY = "google_oauth_state"
SESSION_NEXT_KEY = "google_oauth_next"
SESSION_ACCION_KEY = "google_oauth_accion"


# ---------------------------------------------------------------------
# Construcción del flujo OAuth (compartida por ambos casos de uso)
# ---------------------------------------------------------------------

def _construir_flow():
    client_config = {
        "web": {
            "client_id": settings.GOOGLE_OAUTH_CLIENT_ID,
            "client_secret": settings.GOOGLE_OAUTH_CLIENT_SECRET,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "redirect_uris": [settings.GOOGLE_OAUTH_REDIRECT_URI],
        }
    }

    return Flow.from_client_config(
        client_config,
        scopes=settings.GOOGLE_OAUTH_SCOPES,
        redirect_uri=settings.GOOGLE_OAUTH_REDIRECT_URI,
    )


def _iniciar_flow(request, accion):
    flow = _construir_flow()

    autorizacion_url, estado = flow.authorization_url(
        access_type="offline",
        include_granted_scopes="true",
        prompt="consent",
    )

    request.session[SESSION_STATE_KEY] = estado
    request.session[SESSION_NEXT_KEY] = request.GET.get("next", "/")
    request.session[SESSION_ACCION_KEY] = accion

    return redirect(autorizacion_url)


def _obtener_perfil_google(credenciales):
    """Consulta a Google quién es el usuario dueño de estas credenciales."""
    servicio = build("oauth2", "v2", credentials=credenciales, cache_discovery=False)
    return servicio.userinfo().get().execute()


def _guardar_cuenta_google(usuario, credenciales, email_google):
    CuentaGoogle.objects.update_or_create(
        usuario=usuario,
        defaults={
            "token_acceso": credenciales.token,
            "token_refresco": credenciales.refresh_token,
            "token_uri": credenciales.token_uri,
            "client_id": credenciales.client_id,
            "client_secret": credenciales.client_secret,
            "scopes": ",".join(credenciales.scopes or settings.GOOGLE_OAUTH_SCOPES),
            "expiracion": credenciales.expiry,
            "email_google": email_google,
        },
    )


def _redirigir_segun_rol(usuario):
    if usuario.is_superuser:
        return redirect("administracion:panel_admin")
    if Barbero.objects.filter(email=usuario.email, activo=True).exists():
        return redirect("barberos:panel_barbero")
    return redirect("panel_cliente")


# ---------------------------------------------------------------------
# Flujo 1: conectar calendario estando ya logueado
# ---------------------------------------------------------------------

@login_required
def conectar_google(request):
    """`?next=` indica a dónde regresar después (panel de admin o de barbero)."""
    return _iniciar_flow(request, accion="conectar")


@login_required
def desconectar_google(request):
    CuentaGoogle.objects.filter(usuario=request.user).delete()
    messages.success(request, "Desconectaste tu Google Calendar.")
    return redirect(request.POST.get("next") or request.GET.get("next") or "/")


# ---------------------------------------------------------------------
# Flujo 2: iniciar sesión / registrarse con Google
# ---------------------------------------------------------------------

def iniciar_sesion_google(request):
    """Botón 'Continuar con Google' en login.html y registro.html."""
    return _iniciar_flow(request, accion="login")


def _login_o_registro_con_google(request, credenciales):
    perfil = _obtener_perfil_google(credenciales)
    email = perfil.get("email")

    if not email:
        messages.error(request, "Google no devolvió un correo válido. Intenta de nuevo.")
        return redirect("login")

    usuario = User.objects.filter(email=email).first()
    es_nuevo = usuario is None

    if es_nuevo:
        with transaction.atomic():
            usuario = User.objects.create(
                username=email,
                email=email,
                first_name=perfil.get("given_name", "") or "",
                last_name=perfil.get("family_name", "") or "",
            )
            usuario.set_unusable_password()  # esta cuenta solo entra por Google
            usuario.save()

            Cliente.objects.create(
                user=usuario,
                nombre=perfil.get("name") or email,
                email=email,
            )

    _guardar_cuenta_google(usuario, credenciales, email)
    auth_login(request, usuario, backend="django.contrib.auth.backends.ModelBackend")

    if es_nuevo:
        messages.success(
            request,
            "¡Bienvenido! Creamos tu cuenta con tu Google y tu calendario ya quedó conectado."
        )
    else:
        messages.success(request, "Iniciaste sesión con Google y tu calendario quedó conectado.")

    return _redirigir_segun_rol(usuario)


# ---------------------------------------------------------------------
# Callback único para ambos flujos
# ---------------------------------------------------------------------

def oauth2callback(request):
    estado_guardado = request.session.get(SESSION_STATE_KEY)
    siguiente = request.session.get(SESSION_NEXT_KEY, "/")
    accion = request.session.get(SESSION_ACCION_KEY, "conectar")

    if not estado_guardado or request.GET.get("state") != estado_guardado:
        messages.error(request, "No se pudo validar la conexión con Google. Intenta de nuevo.")
        return redirect(siguiente if accion == "conectar" else "login")

    flow = _construir_flow()
    flow.fetch_token(authorization_response=request.build_absolute_uri())
    credenciales = flow.credentials

    if accion == "login":
        return _login_o_registro_con_google(request, credenciales)

    # accion == "conectar": el usuario ya debe tener sesión iniciada
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión primero.")
        return redirect("login")

    perfil = _obtener_perfil_google(credenciales)
    _guardar_cuenta_google(request.user, credenciales, perfil.get("email", request.user.email))
    messages.success(request, "Tu Google Calendar quedó conectado correctamente.")
    return redirect(siguiente)
