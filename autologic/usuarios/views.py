from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from barberos.models import Barbero
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from clientes.models import Cliente

def login_view(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        password = request.POST.get('password') or ''

        # Los datos ya escritos se devuelven SIEMPRE a la plantilla, para que
        # el formulario no se vacíe cuando hay un error de validación.
        datos = {'email': email}

        # ---- 1. El correo no puede venir vacío ----
        if not email:
            messages.error(request, '❌ Debes escribir tu correo electrónico.')
            return render(request, 'login.html', datos)

        # ---- 2. El correo debe tener un formato válido ----
        try:
            validate_email(email)
        except ValidationError:
            messages.error(
                request,
                '❌ "%s" no es un correo electrónico válido. '
                'Revisa que esté bien escrito (ejemplo: nombre@correo.com).' % email
            )
            return render(request, 'login.html', datos)

        if not password:
            messages.error(request, '❌ Debes escribir tu contraseña.')
            return render(request, 'login.html', datos)

        # ---- 3. El correo debe existir realmente en la base de datos ----
        # Se busca sin distinguir mayúsculas/minúsculas: "Ana@Mail.com" y
        # "ana@mail.com" son la misma cuenta.
        usuario = User.objects.filter(email__iexact=email).first()

        if usuario is None:
            messages.error(
                request,
                '❌ No existe ninguna cuenta registrada con el correo "%s". '
                'Verifica que esté bien escrito o regístrate.' % email
            )
            return render(request, 'login.html', datos)

        if not usuario.is_active:
            # Una cuenta recién registrada está inactiva hasta que la
            # persona abre el enlace que le llegó por correo. Se
            # distingue de una cuenta desactivada por la barbería, que
            # ya llegó a iniciar sesión alguna vez.
            if usuario.last_login is None:
                messages.error(
                    request,
                    '❌ Todavía no has confirmado tu correo. Busca el mensaje '
                    'que te enviamos a "%s" y abre el enlace para activar '
                    'tu cuenta.' % email
                )
            else:
                messages.error(
                    request,
                    '❌ Esta cuenta está desactivada. Comunícate con la barbería.'
                )
            return render(request, 'login.html', datos)

        # Esta cuenta se creó con "Continuar con Google" y nunca tuvo
        # contraseña propia (a propósito, por seguridad). Si intenta
        # entrar aquí con contraseña, avisamos claramente en vez de
        # mostrar un genérico "credenciales inválidas" confuso.
        if not usuario.has_usable_password():
            messages.error(
                request,
                'Esta cuenta se creó con Google. Usa el botón "Continuar con Google" '
                'para iniciar sesión, o entra a tu perfil una vez logueado para crear '
                'una contraseña propia.'
            )
            return render(request, 'login.html', datos)

        # ---- 4. El correo existe: ahora sí se valida la contraseña ----
        user = authenticate(request, username=usuario.username, password=password)

        if user is None:
            messages.error(
                request,
                '❌ La contraseña es incorrecta. Inténtalo de nuevo o usa '
                '"¿Olvidaste tu contraseña?".'
            )
            return render(request, 'login.html', datos)

        login(request, user)

        # SUPERUSUARIO → Admin
        if user.is_superuser:
            return redirect('administracion:panel_admin')

        # BARBERO (por email en modelo Barbero)
        if Barbero.objects.filter(email__iexact=user.email, activo=True).exists():
            return redirect('barberos:panel_barbero')

        # CLIENTE (por defecto)
        return redirect('panel_cliente')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('login')

def registro_view(request):
    return redirect('registro')

def recuperar_contrasena(request):
    if request.method == "POST":
        email = (request.POST.get("email") or "").strip()
        cedula = (request.POST.get("cedula") or "").strip()

        # Se devuelven los datos escritos para no vaciar el formulario.
        datos = {"email": email, "cedula": cedula}

        try:
            validate_email(email)
        except ValidationError:
            messages.error(request, "❌ Ese correo no tiene un formato válido.")
            return render(request, "recuperar_contrasena.html", datos)

        user = User.objects.filter(email__iexact=email).first()

        if user is None:
            messages.error(
                request,
                '❌ No existe ninguna cuenta registrada con el correo "%s".' % email
            )
            return render(request, "recuperar_contrasena.html", datos)

        cliente = Cliente.objects.filter(
            user=user,
            cedula=cedula
        ).first()

        barbero = Barbero.objects.filter(
            email__iexact=email,
            cedula=cedula,
            activo=True
        ).first()

        if not cliente and not barbero:
            messages.error(
                request,
                "❌ La cédula no coincide con la registrada para ese correo."
            )
            return render(request, "recuperar_contrasena.html", datos)

        request.session["recuperar_usuario"] = user.id

        return redirect("cambiar_contrasena")

    return render(request, "recuperar_contrasena.html")


def cambiar_contrasena(request):
    usuario_id = request.session.get("recuperar_usuario")

    if not usuario_id:
        return redirect("recuperar_contrasena")

    if request.method == "POST":
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "cambiar_contrasena.html")

        if len(password) < 6:
            messages.error(request, "La contraseña debe tener al menos 6 caracteres.")
            return render(request, "cambiar_contrasena.html")

        user = User.objects.get(id=usuario_id)
        user.set_password(password)
        user.save()

        del request.session["recuperar_usuario"]

        messages.success(request, "Contraseña actualizada correctamente.")
        return redirect("login")

    return render(request, "cambiar_contrasena.html")