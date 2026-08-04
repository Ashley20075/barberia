from urllib import request
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.models import User
from django.db import IntegrityError
from clientes.models import Cliente
from citas.models import Cita, Servicio
from barberos.models import Barbero
from inventario.models import Producto
from datetime import datetime, timedelta
from django.http import JsonResponse
from django.core.exceptions import ValidationError


@login_required(login_url='login')
def panel_cliente(request):
    cliente, creado = Cliente.objects.get_or_create(
        user=request.user,
        defaults={
            "nombre": f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            "email": request.user.email,
            "telefono": "",
            "cedula": None,
        }
    )

    proximos = Cita.objects.filter(cliente=cliente).exclude(estado="Cancelada")
    historial = Cita.objects.filter(cliente=cliente, estado="Cancelada")
    barberos = Barbero.objects.filter(activo=True)
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()

    return render(request, "dashboard_cliente.html", {
        "nombre": cliente.nombre,
        "proximos": proximos,
        "historial": historial,
        "barberos": barberos,
        "servicios": servicios,
        "productos": productos,
        "cliente": cliente,
    })


@login_required(login_url='login')
def editar_perfil(request):
    cliente = get_object_or_404(Cliente, user=request.user)

    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if email != request.user.email and User.objects.filter(email=email).exists():
            messages.error(request, '❌ Este correo electrónico ya está registrado.')
            return redirect('editar_perfil')

        if cedula != cliente.cedula and Cliente.objects.filter(cedula=cedula).exists():
            messages.error(request, '❌ Esta cédula ya está registrada.')
            return redirect('editar_perfil')

        try:
            user = request.user
            user.first_name = nombre
            user.last_name = apellido
            user.email = email
            user.username = email

            if password:
                if password != confirm_password:
                    messages.error(request, '❌ Las contraseñas no coinciden.')
                    return redirect('editar_perfil')

                if len(password) < 6:
                    messages.error(request, '❌ La contraseña debe tener al menos 6 caracteres.')
                    return redirect('editar_perfil')

                user.set_password(password)
                update_session_auth_hash(request, user)

            user.save()

            cliente.nombre = f"{nombre} {apellido}"
            cliente.cedula = cedula
            cliente.telefono = telefono
            cliente.email = email
            cliente.save()

            try:
                barbero = Barbero.objects.get(email=request.user.email)
                barbero.nombre = f"{nombre} {apellido}"
                barbero.cedula = cedula
                barbero.telefono = telefono
                barbero.email = email
                barbero.save()
            except Barbero.DoesNotExist:
                pass

            messages.success(request, '✅ Perfil actualizado exitosamente.')
            return redirect('panel_cliente')

        except Exception as e:
            messages.error(request, f'❌ Error al actualizar: {str(e)}')
            return redirect('editar_perfil')

    return render(request, 'editar_perfil.html', {'cliente': cliente})


@login_required(login_url='login')
def agendar_cita(request):
    if request.method == "POST":
        adicionales = request.POST.getlist("adicionales")
        productos_seleccionados = request.POST.getlist("productos")

        adicionales_str = ", ".join(adicionales) if adicionales else "Ninguno"
        productos_str = ", ".join(productos_seleccionados) if productos_seleccionados else "Ninguno"

        try:
            cliente = Cliente.objects.get(user=request.user)
            barbero = Barbero.objects.get(id=request.POST.get("barbero"), activo=True)
            servicio = Servicio.objects.get(id=request.POST.get("servicio"))
            duracion_total = int(request.POST.get("duracion_total", 35))
            fecha = request.POST.get("fecha")
            hora = request.POST.get("hora")

        except (Cliente.DoesNotExist, Barbero.DoesNotExist, Servicio.DoesNotExist):
            messages.error(request, "❌ Datos inválidos.")
            return redirect("panel_cliente")

        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

        if not barbero.es_dia_laboral(fecha_obj):
            messages.error(request, f"❌ {barbero.nombre} no trabaja en esa fecha.")
            return redirect("panel_cliente")

        if barbero.es_dia_descanso(fecha_obj):
            messages.error(request, f"❌ {barbero.nombre} tiene descanso en esa fecha.")
            return redirect("panel_cliente")

        # Un cliente solo puede tener una cita por día
        cita_cliente = Cita.objects.filter(
            cliente=cliente,
            fecha=fecha
        ).exclude(
            estado="Cancelada"
        ).first()

        if cita_cliente:
            messages.error(request, "❌ Ya tienes una cita programada para ese día.")
            return redirect("panel_cliente")

        # Validación de solapamiento de horarios para el barbero
        inicio_nueva = datetime.strptime(hora, "%I:%M %p")
        fin_nueva = inicio_nueva + timedelta(minutes=duracion_total)

        citas = Cita.objects.filter(
            barbero=barbero,
            fecha=fecha,
            estado__in=["Pendiente", "Confirmada"]
        )

        for cita in citas:
            inicio = datetime.strptime(cita.hora, "%I:%M %p")
            fin = inicio + timedelta(minutes=cita.duracion_total)

            if inicio_nueva < fin and fin_nueva > inicio:
                messages.error(request, "❌ Ese horario se cruza con otra cita.")
                return redirect("panel_cliente")

        try:
            Cita.objects.create(
                cliente=cliente,
                servicio=servicio,
                barbero=barbero,
                adicionales=adicionales_str,
                productos=productos_str,
                fecha=fecha,
                hora=hora,
                duracion_total=duracion_total,
                estado="Pendiente",
            )
            
            # Disminuir el stock de los productos seleccionados
            for nombre_producto in productos_seleccionados:
                try:
                    producto = Producto.objects.get(nombre=nombre_producto)
                    if producto.stock_actual > 0:
                        producto.stock_actual -= 1
                        producto.save()
                except Producto.DoesNotExist:
                    pass
            
            messages.success(request, f"✅ Cita agendada exitosamente con {barbero.nombre}.")
            return redirect("panel_cliente")

        except ValidationError as e:
            messages.error(request, f"❌ {e.messages[0]}")
            return redirect("panel_cliente")

        except IntegrityError:
            messages.error(request, "❌ Ese horario ya fue reservado.")
            return redirect("panel_cliente")

    # Si no es POST, redirigir al panel
    return redirect("panel_cliente")


@login_required(login_url='login')
def cancelar_cita_cliente(request, id):
    cita = get_object_or_404(Cita, id=id)

    if cita.estado != "Cancelada":
        if cita.productos and cita.productos != "Ninguno":
            productos = cita.productos.split(",")

            for nombre_producto in productos:
                nombre_producto = nombre_producto.strip()
                try:
                    producto = Producto.objects.get(nombre=nombre_producto)
                    producto.stock_actual += 1
                    producto.save()
                except Producto.DoesNotExist:
                    pass

        cita.estado = "Cancelada"
        cita.save()

        messages.success(request, "✅ Cita cancelada exitosamente")

    return redirect("panel_cliente")


def registro(request):
    if request.method == "POST":
        nombre = request.POST.get("nombre")
        apellido = request.POST.get("apellido")
        cedula = request.POST.get("cedula")
        telefono = request.POST.get("telefono")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        if password != confirm_password:
            messages.error(request, "Las contraseñas no coinciden")
            return render(request, "registro.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "Este correo electrónico ya está registrado")
            return render(request, "registro.html")

        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
            )

            Cliente.objects.create(
                user=user,
                nombre=f"{nombre} {apellido}",
                cedula=cedula,
                telefono=telefono,
                email=email,
            )

            messages.success(request, "¡Cuenta creada exitosamente! Ahora inicia sesión.")
            return redirect("login")

        except Exception as e:
            messages.error(request, f"Error al crear usuario: {e}")
            return render(request, "registro.html")

    return render(request, "registro.html")


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada exitosamente")
    return redirect("login")


@login_required(login_url='login')
def eliminar_cuenta(request):
    if request.method == "POST":
        usuario = request.user
        usuario.delete()
        return redirect("cuenta_eliminada")

    return redirect("panel_cliente")


def cuenta_eliminada(request):
    return render(request, "cuenta_eliminada.html")


@login_required(login_url="login")
def horarios_disponibles(request):
    fecha = request.GET.get("fecha")
    barbero_id = request.GET.get("barbero")
    adicionales = request.GET.getlist("adicionales")

    if not fecha or not barbero_id:
        return JsonResponse([], safe=False)

    fecha = datetime.strptime(fecha, "%Y-%m-%d").date()

    barbero = get_object_or_404(
        Barbero,
        id=barbero_id,
        activo=True
    )

    duracion = 35

    if "Arreglo de barba" in adicionales:
        duracion += 5

    if "Cejas" in adicionales:
        duracion += 5

    if "Diseño y líneas" in adicionales:
        duracion += 5

    horarios = barbero.horarios_disponibles(fecha, duracion)

    return JsonResponse(horarios, safe=False)