from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.models import User
from barberos.models import Barbero
from django.contrib.auth.hashers import make_password
from clientes.models import Cliente

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            usuario = User.objects.get(email=email)
            username = usuario.username
        except User.DoesNotExist:
            messages.error(request, 'Credenciales inválidas')
            return render(request, 'login.html')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)

            # SUPERUSUARIO → Admin
            if user.is_superuser:
                return redirect('administracion:panel_admin')

            # BARBERO (por email en modelo Barbero)
            try:
                barbero = Barbero.objects.get(email=user.email, activo=True)
                return redirect('barberos:panel_barbero')
            except Barbero.DoesNotExist:
                pass

            # CLIENTE (por defecto)
            return redirect('panel_cliente')

        messages.error(request, 'Credenciales inválidas')
        return render(request, 'login.html')

    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.info(request, 'Sesión cerrada exitosamente')
    return redirect('login')

def registro_view(request):
    return redirect('registro')

def recuperar_contrasena(request):
    if request.method == "POST":
        email = request.POST.get("email")
        cedula = request.POST.get("cedula")

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")
            return render(request, "recuperar_contrasena.html")

        cliente = Cliente.objects.filter(
            user=user,
            cedula=cedula
        ).first()

        barbero = Barbero.objects.filter(
            email=email,
            cedula=cedula,
            activo=True
        ).first()

        if not cliente and not barbero:
            messages.error(request, "Los datos no coinciden.")
            return render(request, "recuperar_contrasena.html")

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