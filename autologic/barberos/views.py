from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from citas.models import Cita
from inventario.models import Producto
from .models import Barbero
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet
from django.conf import settings
import os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db import transaction
from clientes.models import Cliente
from googlecalendar.models import CuentaGoogle

@login_required(login_url='login')
def panel_barbero(request):

    try:
        barbero = Barbero.objects.get(
            email=request.user.email,
            activo=True
        )

    except Barbero.DoesNotExist:
        messages.error(
            request,
            "No tienes un perfil de barbero asignado."
        )
        return redirect("inicio")

    hoy = timezone.now().date()

    if not barbero.es_dia_laboral(hoy) or barbero.es_dia_descanso(hoy):
        messages.warning(
            request,
            f"⚠️ Hoy es día de descanso o no laboral para {barbero.nombre}."
        )

    proximas_citas = Cita.objects.filter(
        barbero=barbero,
        estado__in=[
            "Pendiente",
            "Confirmada"
        ]
    ).order_by(
        "fecha",
        "hora"
    )

    historial_citas = Cita.objects.filter(
        barbero=barbero,
        estado__in=[
            "Finalizada",
            "Cancelada"
        ]
    ).order_by(
        "-fecha",
        "-hora"
    )

    total_citas = Cita.objects.filter(
        barbero=barbero
    ).count()

    citas_pendientes = proximas_citas.filter(
        estado="Pendiente"
    ).count()

    citas_confirmadas = proximas_citas.filter(
        estado="Confirmada"
    ).count()

    citas_canceladas = historial_citas.filter(
        estado="Cancelada"
    ).count()

    citas_finalizadas = historial_citas.filter(
        estado="Finalizada"
    ).count()

    context = {
        "barbero": barbero,

        "proximas_citas": proximas_citas,
        "historial_citas": historial_citas,

        "total_citas": total_citas,
        "citas_pendientes": citas_pendientes,
        "citas_confirmadas": citas_confirmadas,
        "citas_canceladas": citas_canceladas,
        "citas_finalizadas": citas_finalizadas,

        "cuenta_google": CuentaGoogle.objects.filter(usuario=request.user).first(),
    }

    return render(
        request,
        "dashboard_barbero.html",
        context
    )

@login_required(login_url='login')
def confirmar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    
    try:
        barbero = Barbero.objects.get(email=request.user.email, activo=True)
        if cita.barbero != barbero:
            messages.error(request, '❌ No tienes permiso para confirmar esta cita.')
            return redirect('barberos:panel_barbero')
    except Barbero.DoesNotExist:
        messages.error(request, '❌ No tienes un perfil de barbero asignado.')
        return redirect('barberos:panel_barbero')
    
    if cita.estado == "Pendiente":
        # ===== VALIDACIÓN: Verificar que el barbero trabaja en esa fecha =====
        if not barbero.es_dia_laboral(cita.fecha):
            messages.error(request, f'❌ {barbero.nombre} no trabaja en esa fecha.')
            return redirect('barberos:panel_barbero')
        
        if barbero.es_dia_descanso(cita.fecha):
            messages.error(request, f'❌ {barbero.nombre} tiene descanso en esa fecha.')
            return redirect('barberos:panel_barbero')
        
        cita.estado = "Confirmada"
        cita.save()
        messages.success(request, f'✅ Cita de {cita.cliente.nombre} confirmada.')
    
    return redirect('barberos:panel_barbero')

@login_required(login_url='login')
def cancelar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)
    
    try:
        barbero = Barbero.objects.get(email=request.user.email, activo=True)
        if cita.barbero != barbero:
            messages.error(request, '❌ No tienes permiso para cancelar esta cita.')
            return redirect('barberos:panel_barbero')
    except Barbero.DoesNotExist:
        messages.error(request, '❌ No tienes un perfil de barbero asignado.')
        return redirect('barberos:panel_barbero')

    if cita.estado != "Cancelada":
        if cita.productos and cita.productos != "Ninguno":
            productos = cita.productos.split(',')
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
        messages.success(request, f'✅ Cita de {cita.cliente.nombre} cancelada.')

    return redirect('barberos:panel_barbero')

@login_required(login_url='login')
def finalizar_cita(request, id):
    cita = get_object_or_404(Cita, id=id)

    try:
        barbero = Barbero.objects.get(
            email=request.user.email,
            activo=True
        )

        if cita.barbero != barbero:
            messages.error(
                request,
                '❌ No tienes permiso para finalizar esta cita.'
            )
            return redirect('barberos:panel_barbero')

    except Barbero.DoesNotExist:
        messages.error(
            request,
            '❌ No tienes un perfil de barbero asignado.'
        )
        return redirect('barberos:panel_barbero')

    if cita.estado == "Confirmada":
        cita.estado = "Finalizada"
        cita.save()
        messages.success(
            request,
            f'✅ Cita de {cita.cliente.nombre} finalizada.'
        )

    return redirect('barberos:panel_barbero')

@login_required
def lista_barberos(request):
    barberos = Barbero.objects.filter(activo=True)
    return render(request, 'barberos/lista.html', {'barberos': barberos})

@login_required
def detalle_barbero(request, id):
    barbero = get_object_or_404(Barbero, id=id)
    return render(request, 'barberos/detalle.html', {'barbero': barbero})

@login_required(login_url='login')
def editar_perfil_barbero(request):
    barbero = get_object_or_404(
        Barbero,
        email=request.user.email
    )

    if request.method == 'POST':

        nombre = request.POST.get('nombre', '').strip()
        apellido = request.POST.get('apellido', '').strip()
        cedula = request.POST.get('cedula', '').strip()
        telefono = request.POST.get('telefono', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')

        if email != request.user.email and User.objects.filter(email=email).exists():
            messages.error(request, '❌ Este correo ya está registrado.')
            return redirect('barberos:editar_perfil_barbero')

        try:

            with transaction.atomic():

                user = request.user

                user.first_name = nombre
                user.last_name = apellido
                user.username = email
                user.email = email

                if password:

                    if password != confirm_password:
                        messages.error(request, '❌ Las contraseñas no coinciden.')
                        return redirect('barberos:editar_perfil_barbero')

                    if len(password) < 6:
                        messages.error(request, '❌ La contraseña debe tener al menos 6 caracteres.')
                        return redirect('barberos:editar_perfil_barbero')

                    user.set_password(password)
                    update_session_auth_hash(request, user)

                user.save()

                # Actualizar datos del barbero
                barbero.nombre = f"{nombre} {apellido}".strip()
                barbero.cedula = cedula
                barbero.telefono = telefono
                barbero.email = email
                barbero.save()

                # Si existe cliente asociado también lo actualiza
                Cliente.objects.filter(user=request.user).update(
                    nombre=f"{nombre} {apellido}".strip(),
                    cedula=cedula,
                    telefono=telefono,
                    email=email
                )

            messages.success(request, "✅ Perfil actualizado correctamente.")
            return redirect("barberos:panel_barbero")

        except Exception as e:
            messages.error(request, f"❌ {e}")
            return redirect("barberos:editar_perfil_barbero")

    nombre = barbero.nombre.split()

    return render(
        request,
        "editar_perfil_barbero.html",
        {
            "barbero": barbero,
            "nombre": nombre[0] if len(nombre) > 0 else "",
            "apellido": " ".join(nombre[1:]) if len(nombre) > 1 else "",
        }
    )