from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from citas.models import Cita
from inventario.models import Producto
from inventario.utils import registrar_movimiento
from .models import Barbero
from django.utils import timezone
from datetime import datetime, timedelta
from django.http import HttpResponse
from django.views.decorators.cache import never_cache
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image # pyright: ignore[reportMissingModuleSource]
from reportlab.lib.styles import getSampleStyleSheet # type: ignore
from django.conf import settings
from twilio.rest import Client # type: ignore
import os
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.db import IntegrityError, transaction
from clientes.models import Cliente
from googlecalendar.models import CuentaGoogle
from citas.paginacion import paginar
from notificaciones.utils import notificar, usuario_de_cliente

@never_cache
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

    # Filtros enviados desde el formulario.
    filtro_estado = request.GET.get('estado', '').strip()
    filtro_fecha_inicio = request.GET.get('fecha_inicio', '').strip()
    filtro_fecha_fin = request.GET.get('fecha_fin', '').strip()

    # Base de citas activas y de historial del barbero.
    citas_base = Cita.objects.filter(barbero=barbero)

    # Aplicar filtros sobre el conjunto de citas.
    if filtro_estado:
        citas_base = citas_base.filter(estado=filtro_estado)

    if filtro_fecha_inicio:
        try:
            fecha_inicio = datetime.strptime(
                filtro_fecha_inicio, '%Y-%m-%d'
            ).date()
            citas_base = citas_base.filter(fecha__gte=fecha_inicio)
        except ValueError:
            filtro_fecha_inicio = ''

    if filtro_fecha_fin:
        try:
            fecha_fin = datetime.strptime(
                filtro_fecha_fin, '%Y-%m-%d'
            ).date()
            citas_base = citas_base.filter(fecha__lte=fecha_fin)
        except ValueError:
            filtro_fecha_fin = ''

    # Mostrar las citas filtradas, sin mezclar el historial archivado.
    proximas_citas = citas_base.filter(
        estado__in=['Pendiente', 'Confirmada']
    ).order_by('fecha', 'hora')

    historial_citas = citas_base.filter(
        estado__in=['Finalizada', 'Cancelada'],
        historial_archivado=False
    ).order_by('-fecha', '-hora')

    historial_citas = Cita.objects.filter(
        barbero=barbero,
        estado__in=["Finalizada", "Cancelada"],
        historial_archivado=False
).order_by("-fecha", "-hora")

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
        "historial_citas": paginar(historial_citas, request, parametro="pagina_historial"),

        "total_citas": total_citas,
        "citas_pendientes": citas_pendientes,
        "citas_confirmadas": citas_confirmadas,
        "citas_canceladas": citas_canceladas,
        "citas_finalizadas": citas_finalizadas,

        "filtro_estado": filtro_estado,
        "filtro_fecha_inicio": filtro_fecha_inicio,
        "filtro_fecha_fin": filtro_fecha_fin,

        "cuenta_google": CuentaGoogle.objects.filter(usuario=request.user).first(),
        "notificaciones_no_leidas": request.user.notificaciones.filter(leida=False).count(),
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
                    registrar_movimiento(
                        producto=producto,
                        tipo='ENTRADA',
                        cantidad=1,
                        usuario=request.user,
                        nota=f'Devolución por cancelación de cita de {cita.cliente.nombre}',
                    )
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

        # ============================================================
        # PROGRAMA DE FIDELIDAD: cada 10 cortes finalizados, el
        # siguiente corte queda gratis para el cliente.
        # ============================================================
        cliente = cita.cliente
        cliente.cortes_completados += 1
        cliente.cortes_para_recompensa += 1

        gano_recompensa = False
        if cliente.cortes_para_recompensa >= 10:
            cliente.cortes_para_recompensa = 0
            cliente.recompensas_disponibles += 1
            gano_recompensa = True

        cliente.save()

        if gano_recompensa:
            usuario_cliente = usuario_de_cliente(cliente)
            notificar(
                usuario_cliente,
                '🎉 ¡Felicitaciones! Completaste 10 cortes. '
                'Tu próximo corte será gratis.',
                cita=cita,
            )

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
        email = request.POST.get('email', '').strip().lower()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')
        dia_descanso = request.POST.get('dia_descanso', '').strip()

        nombre_completo = f'{nombre} {apellido}'.strip()

        # Validar los campos obligatorios.
        if not all([nombre, apellido, cedula, telefono, email]):
            messages.error(
                request,
                'Completa todos los campos obligatorios.'
            )
            return redirect('barberos:editar_perfil_barbero')

        # Validar el correo en otras cuentas de usuario.
        if User.objects.filter(email__iexact=email).exclude(
            pk=request.user.pk
        ).exists():
            messages.error(
                request,
                'Ese correo ya pertenece a otra cuenta.'
            )
            return redirect('barberos:editar_perfil_barbero')

        # Validar el correo en otros perfiles de barbero.
        if Barbero.objects.filter(email__iexact=email).exclude(
            pk=barbero.pk
        ).exists():
            messages.error(
                request,
                'Ese correo ya está asignado a otro barbero.'
            )
            return redirect('barberos:editar_perfil_barbero')

        # Validar la cédula en otros perfiles.
        if Barbero.objects.filter(cedula=cedula).exclude(
            pk=barbero.pk
        ).exists():
            messages.error(
                request,
                'Esa cédula ya está registrada para otro barbero.'
            )
            return redirect('barberos:editar_perfil_barbero')

        # Validar el día de descanso.
        dias_validos = dict(Barbero.DIAS_SEMANA)
        if dia_descanso not in dias_validos:
            messages.error(
                request,
                'Selecciona un día de descanso válido.'
            )
            return redirect('barberos:editar_perfil_barbero')

        # La contraseña es opcional.
        if password or confirm_password:
            if not password or not confirm_password:
                messages.error(
                    request,
                    'Completa los dos campos de contraseña.'
                )
                return redirect('barberos:editar_perfil_barbero')

            if password != confirm_password:
                messages.error(
                    request,
                    'Las contraseñas no coinciden.'
                )
                return redirect('barberos:editar_perfil_barbero')

            if len(password) < 6:
                messages.error(
                    request,
                    'La contraseña debe tener al menos 6 caracteres.'
                )
                return redirect('barberos:editar_perfil_barbero')

        try:
            with transaction.atomic():
                user = User.objects.select_for_update().get(
                    pk=request.user.pk
                )

                user.first_name = nombre
                user.last_name = apellido
                user.email = email

                # No modificar el nombre de usuario si el proyecto
                # permite iniciar sesión con un username diferente.
                # Si tu proyecto usa el correo como username, sincronizarlo.
                if user.username == request.user.email:
                    user.username = email

                if password:
                    user.set_password(password)

                user.save()

                barbero.nombre = nombre_completo
                barbero.cedula = cedula
                barbero.telefono = telefono
                barbero.email = email
                barbero.dia_descanso = dia_descanso
                barbero.save()

                # Actualizar el perfil de cliente asociado, si existe.
                Cliente.objects.filter(user=user).update(
                    nombre=nombre_completo,
                    telefono=telefono,
                    email=email
                )
                # No asignar la cédula al cliente si pertenece a otro
                # registro; se evita sobrescribir datos ajenos.
                Cliente.objects.filter(
                    user=user
                ).exclude(
                    cedula=cedula
                ).update(cedula=cedula)

            if password:
                update_session_auth_hash(request, user)

            messages.success(
                request,
                'Perfil actualizado correctamente.'
            )
            return redirect('barberos:editar_perfil_barbero')
        except IntegrityError:
            messages.error(
                request,
                'No se pudo guardar: el correo o la cédula '
                'pueden estar registrados en otra cuenta.'
            )
            return redirect('barberos:editar_perfil_barbero')
    nombre_partes = barbero.nombre.split()
    return render(
        request,
        'editar_perfil_barbero.html',
        {
            'barbero': barbero,
            'nombre': nombre_partes[0] if nombre_partes else '',
            'apellido': ' '.join(nombre_partes[1:]),
            'dias_semana': Barbero.DIAS_SEMANA,
            'notificaciones_no_leidas': (
                request.user.notificaciones.filter(leida=False).count()
            ),
        }
    )
@login_required(login_url='login')
def vaciar_historial_barbero(request):
    if request.method != 'POST':
        return redirect('barberos:panel_barbero')

    barbero = get_object_or_404(
        Barbero,
        email=request.user.email,
        activo=True
    )

    cantidad = Cita.objects.filter(
        barbero=barbero,
        estado__in=['Finalizada', 'Cancelada'],
        historial_archivado=False
    ).update(historial_archivado=True)

    if cantidad:
        messages.success(
            request,
            f'Se archivaron {cantidad} citas de tu historial.'
        )
    else:
        messages.info(
            request,
            'No tienes citas finalizadas o canceladas pendientes por archivar.'
        )

    return redirect('barberos:panel_barbero')
