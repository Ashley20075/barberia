from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from citas.models import Cita, Servicio
from clientes.models import Cliente
from barberos.models import Barbero
from inventario.models import Producto
from datetime import datetime
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.conf import settings
import os
from googlecalendar.models import CuentaGoogle
from .reportes import calcular_cierre_caja

@login_required
def panel_admin(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('inicio')
    
    usuarios = User.objects.all()
    clientes = Cliente.objects.all()
    grupo_barberos, _ = Group.objects.get_or_create(name='Barberos')
    cantidad_barberos = User.objects.filter(groups=grupo_barberos).count()
    barberos = Barbero.objects.all()
    servicios = Servicio.objects.all()
    productos = Producto.objects.all()
    
    citas_activas = Cita.objects.filter(
        estado__in=[
            "Pendiente",
            "Confirmada",
        ]
    ).order_by(
        "-fecha",
        "-hora"
    )

    historial_citas = Cita.objects.filter(
        estado__in=[
            "Finalizada",
            "Cancelada",
        ]
    ).order_by(
        "-fecha",
        "-hora"
    )

    total_citas = Cita.objects.filter(
    estado__in=[
        "Pendiente",
        "Confirmada",
    ]
).count()
    
    context = {
        'usuarios': usuarios,
        'clientes': clientes,
        "citas": citas_activas,
        "historial_citas": historial_citas,
        'barberos': barberos,
        'servicios': servicios,
        'productos': productos,
        'cantidad_barberos': cantidad_barberos,
        "total_citas": total_citas,
        "cuenta_google": CuentaGoogle.objects.filter(usuario=request.user).first(),
    }
    return render(request, 'administracion/panel_administrador.html', context)

@login_required
def asignar_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')

    user = get_object_or_404(User, id=id)
    cliente = Cliente.objects.filter(user=user).first()

    if Barbero.objects.filter(email=user.email).exists():
        messages.warning(request, f'⚠️ El usuario "{user.username}" ya es barbero.')
        return redirect('administracion:panel_admin')

    # Las cuentas creadas con "Continuar con Google" no traen cédula
    # (Google no la conoce), así que el modal "Hacer barbero" del panel
    # deja completarla aquí en vez de bloquear la acción.
    cedula = (request.POST.get('cedula') or (cliente.cedula if cliente else '') or '').strip()
    telefono = (request.POST.get('telefono') or (cliente.telefono if cliente else '') or '').strip()
    especialidad = (request.POST.get('especialidad') or 'General').strip()

    if not cedula:
        messages.error(
            request,
            f'❌ Para hacer barbero a "{user.username}" primero debes ingresar su cédula '
            'en el formulario de "Hacer barbero".'
        )
        return redirect('administracion:panel_admin')

    if Barbero.objects.filter(cedula=cedula).exists():
        messages.warning(request, '⚠️ Ya existe un barbero registrado con esa cédula.')
        return redirect('administracion:panel_admin')

    # Solo tocamos el grupo/rol una vez que TODAS las validaciones pasaron,
    # para no dejar al usuario marcado como "Barbero" sin un registro
    # de Barbero real detrás (eso pasaba antes: el grupo se asignaba
    # primero y las validaciones podían fallar después).
    grupo, _ = Group.objects.get_or_create(name='Barberos')
    user.groups.add(grupo)

    # Aprovechamos para completar los datos del cliente si le faltaban
    if cliente:
        cambios = False
        if not cliente.cedula:
            cliente.cedula = cedula
            cambios = True
        if telefono and not cliente.telefono:
            cliente.telefono = telefono
            cambios = True
        if cambios:
            cliente.save()

    Barbero.objects.create(
        nombre=cliente.nombre if cliente else (user.get_full_name() or user.username),
        cedula=cedula,
        telefono=telefono,
        email=user.email,
        especialidad=especialidad,
        activo=True,
        jornada_inicio='08:00',
        jornada_fin='18:00',
        duracion_cita=30,
        dias_laborales='LUN,MAR,MIE,JUE,VIE,SAB',
        dia_descanso='DOM',
        tiempo_entre_citas=15
    )

    messages.success(request, f'✅ Usuario "{user.username}" ahora es barbero.')
    return redirect('administracion:panel_admin')

@login_required
def quitar_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    user = get_object_or_404(User, id=id)
    grupo = Group.objects.get(name='Barberos')
    user.groups.remove(grupo)
    Barbero.objects.filter(email=user.email).delete()
    
    messages.success(request, f'✅ Usuario "{user.username}" ya no es barbero.')
    return redirect('administracion:panel_admin')

@login_required
def desactivar_usuario(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    usuario = get_object_or_404(User, id=id)
    usuario.is_active = False
    usuario.save()
    messages.success(request, f'✅ El usuario "{usuario.username}" fue desactivado.')
    return redirect('administracion:panel_admin')

@login_required
def activar_usuario(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    usuario = get_object_or_404(User, id=id)
    usuario.is_active = True
    usuario.save()
    messages.success(request, f'✅ El usuario "{usuario.username}" fue activado.')
    return redirect('administracion:panel_admin')

@login_required
def crear_usuario(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    if request.method == 'POST':
        nombre = request.POST.get('nombre')
        apellido = request.POST.get('apellido')
        cedula = request.POST.get('cedula')
        telefono = request.POST.get('telefono')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        if password != confirm_password:
            messages.error(request, '❌ Las contraseñas no coinciden')
            return redirect('administracion:panel_admin')
        
        if User.objects.filter(email=email).exists():
            messages.error(request, '❌ Este correo ya está registrado')
            return redirect('administracion:panel_admin')
        
        if Cliente.objects.filter(cedula=cedula).exists():
            messages.error(request, '❌ La cédula ya está registrada')
            return redirect('administracion:panel_admin')
        
        try:
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido
            )
            Cliente.objects.create(
                user=user,
                nombre=f"{nombre} {apellido}",
                cedula=cedula,
                telefono=telefono,
                email=email
            )
            messages.success(request, f'✅ Usuario "{nombre} {apellido}" creado correctamente.')
        except Exception as e:
            messages.error(request, f'❌ {e}')
        return redirect('administracion:panel_admin')
    return redirect('administracion:panel_admin')

@login_required
def editar_cita(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    cita = get_object_or_404(Cita, id=id)
    if request.method == 'POST':
        cliente_id = request.POST.get('cliente')
        servicio_id = request.POST.get('servicio')
        barbero_id = request.POST.get('barbero')
        fecha = request.POST.get('fecha')
        hora = request.POST.get('hora')
        estado = request.POST.get('estado')
        
        cliente = get_object_or_404(Cliente, id=cliente_id)
        servicio = get_object_or_404(Servicio, id=servicio_id)
        barbero = get_object_or_404(Barbero, id=barbero_id)
        
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
        
        if not barbero.es_dia_laboral(fecha_obj):
            messages.error(request, f'❌ {barbero.nombre} no trabaja en esa fecha.')
            return redirect('administracion:panel_admin')
        
        if barbero.es_dia_descanso(fecha_obj):
            messages.error(request, f'❌ {barbero.nombre} tiene descanso en esa fecha.')
            return redirect('administracion:panel_admin')
        
        cita_existente = Cita.objects.filter(
            barbero=barbero,
            fecha=fecha,
            hora=hora
        ).exclude(id=id).exclude(estado='Cancelada').exists()
        
        if cita_existente:
            messages.error(request, f'❌ El barbero ya tiene una cita en ese horario.')
            return redirect('administracion:panel_admin')

        cita.cliente = cliente
        cita.servicio = servicio
        cita.barbero = barbero
        cita.fecha = fecha
        cita.hora = hora
        cita.estado = estado
        cita.save()
        # La sincronización con Google Calendar (incluida la reasignación
        # de barbero) la hace automáticamente la señal post_save.

        messages.success(request, '✅ Cita actualizada correctamente.')
        return redirect('administracion:panel_admin')
    return redirect('administracion:panel_admin')

@login_required
def eliminar_cita(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    cita = get_object_or_404(Cita, id=id)
    cita.delete()
    # El evento de Google Calendar se borra automáticamente
    # (señal pre_delete en googlecalendar/signals.py).
    messages.success(request, '✅ Cita eliminada correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def agregar_barbero(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    if request.method == 'POST':
        try:
            cedula = request.POST.get('cedula')
            email = request.POST.get('email')
            
            if Barbero.objects.filter(cedula=cedula).exists():
                messages.error(request, f'❌ La cédula "{cedula}" ya está registrada.')
                return redirect('administracion:panel_admin')
            
            if Barbero.objects.filter(email=email).exists():
                messages.error(request, f'❌ El email "{email}" ya está registrado.')
                return redirect('administracion:panel_admin')
            
            barbero = Barbero.objects.create(
                nombre=request.POST.get('nombre'),
                cedula=cedula,
                especialidad=request.POST.get('especialidad'),
                telefono=request.POST.get('telefono'),
                email=email,
                activo=True,
                jornada_inicio=request.POST.get('jornada_inicio', '08:00'),
                jornada_fin=request.POST.get('jornada_fin', '18:00'),
                duracion_cita=int(request.POST.get('duracion_cita', 30)),
                dias_laborales=request.POST.get('dias_laborales', 'LUN,MAR,MIE,JUE,VIE,SAB'),
                dia_descanso=request.POST.get('dia_descanso', 'DOM'),
                tiempo_entre_citas=int(request.POST.get('tiempo_entre_citas', 15))
            )
            messages.success(request, f'✅ Barbero "{barbero.nombre}" agregado correctamente.')
        except Exception as e:
            messages.error(request, f'❌ Error: {e}')
        return redirect('administracion:panel_admin')
    return redirect('administracion:panel_admin')

@login_required
def editar_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    barbero = get_object_or_404(Barbero, id=id)
    
    if request.method == 'POST':
        try:
            barbero.nombre = request.POST.get('nombre', '').strip()
            barbero.cedula = request.POST.get('cedula', '').strip()
            barbero.especialidad = request.POST.get('especialidad', '').strip()
            barbero.telefono = request.POST.get('telefono', '').strip()
            barbero.email = request.POST.get('email', '').strip()
            barbero.activo = request.POST.get('activo') == 'on'
            
            # Horarios
            jornada_inicio = request.POST.get('jornada_inicio', '08:00')
            jornada_fin = request.POST.get('jornada_fin', '18:00')
            
            if jornada_inicio and jornada_fin:
                barbero.jornada_inicio = jornada_inicio
                barbero.jornada_fin = jornada_fin
            
            try:
                barbero.duracion_cita = int(request.POST.get('duracion_cita', 30))
            except ValueError:
                barbero.duracion_cita = 30
                
            try:
                barbero.tiempo_entre_citas = int(request.POST.get('tiempo_entre_citas', 15))
            except ValueError:
                barbero.tiempo_entre_citas = 15
            
            barbero.dia_descanso = request.POST.get('dia_descanso', 'DOM')
            
            # Días laborales
            dias_laborales = request.POST.getlist('dias_laborales')
            
            if dias_laborales:
                dias_limpios = [d.strip() for d in dias_laborales if d.strip()]
                barbero.dias_laborales = ','.join(dias_limpios)
            else:
                barbero.dias_laborales = 'LUN,MAR,MIE,JUE,VIE,SAB'
            
            barbero.save()
            messages.success(request, f'✅ Barbero "{barbero.nombre}" actualizado correctamente.')
            
        except Exception as e:
            messages.error(request, f'❌ Error al actualizar: {str(e)}')
        
        return redirect('administracion:panel_admin')
    
    return redirect('administracion:panel_admin')

@login_required
def eliminar_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    barbero = get_object_or_404(Barbero, id=id)
    nombre = barbero.nombre
    barbero.delete()
    messages.success(request, f'✅ Barbero "{nombre}" eliminado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def agregar_producto(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    if request.method == 'POST':
        try:
            producto = Producto(
                nombre=request.POST.get("nombre"),
                precio_unitario=request.POST.get("precio"),
                stock_actual=request.POST.get("stock")
            )

            producto.full_clean()
            producto.save()

            messages.success(
                request,
                f'✅ Producto "{producto.nombre}" agregado correctamente.'
            )

        except ValidationError as e:
            messages.error(
                request,
                e.messages[0]
            )

    return redirect('administracion:panel_admin')

@login_required
def editar_producto(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    producto = get_object_or_404(Producto, id=id)
    if request.method == 'POST':
        producto.nombre = request.POST.get('nombre')
        producto.precio_unitario = request.POST.get('precio')
        producto.stock_actual = request.POST.get('stock')
        try:
            producto.full_clean()
            producto.save()
            messages.success(
                request,
                    "✅ Producto actualizado correctamente."
            )
        except ValidationError as e:
                messages.error(
                    request,
                    e.messages[0]
                )
        messages.success(request, '✅ Producto actualizado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def eliminar_producto_admin(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    producto = get_object_or_404(Producto, id=id)
    nombre = producto.nombre
    producto.delete()
    messages.success(request, f'✅ Producto "{nombre}" eliminado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def agregar_servicio(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    if request.method == 'POST':
        Servicio.objects.create(
            nombre=request.POST.get('nombre'),
            descripcion=request.POST.get('descripcion'),
            precio=request.POST.get('precio'),
            duracion=request.POST.get('duracion')
        )
        messages.success(request, f'✅ Servicio "{request.POST.get("nombre")}" agregado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def editar_servicio(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    servicio = get_object_or_404(Servicio, id=id)
    if request.method == 'POST':
        servicio.nombre = request.POST.get('nombre')
        servicio.descripcion = request.POST.get('descripcion')
        servicio.precio = request.POST.get('precio')
        servicio.duracion = request.POST.get('duracion')
        servicio.save()
        messages.success(request, '✅ Servicio actualizado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def eliminar_servicio(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    servicio = get_object_or_404(Servicio, id=id)
    nombre = servicio.nombre
    servicio.delete()
    messages.success(request, f'✅ Servicio "{nombre}" eliminado correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def certificado_barbero_admin(request, id):

    if not request.user.is_superuser:
        messages.error(
            request,
            "No tienes permisos."
        )
        return redirect("administracion:panel_admin")

    barbero = get_object_or_404(
        Barbero,
        id=id
    )

    response = HttpResponse(
        content_type='application/pdf'
    )

    response['Content-Disposition'] = (
        f'attachment; filename="certificado_{barbero.nombre}.pdf"'
    )

    doc = SimpleDocTemplate(response)

    estilos = getSampleStyleSheet()

    elementos = []

    ruta_logo = os.path.join(
        settings.BASE_DIR,
        "inventario",
        "static",
        "img",
        "logo.jpeg"
    )

    if os.path.exists(ruta_logo):

        logo = Image(ruta_logo)

        logo.drawWidth = 80
        logo.drawHeight = 80

        elementos.append(logo)

    elementos.append(
        Paragraph(
            "<b>CERTIFICADO LABORAL</b>",
            estilos["Title"]
        )
    )

    elementos.append(
        Paragraph(
            "BarberSpringfield",
            estilos["Heading2"]
        )
    )

    elementos.append(
        Paragraph(
            "<br/><br/>Se certifica que:",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"<b>{barbero.nombre}</b>",
            estilos["Heading1"]
        )
    )

    elementos.append(
        Paragraph(
            f"Cédula: {barbero.cedula}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Especialidad: {barbero.especialidad}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"Correo: {barbero.email}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "<br/>Actualmente se encuentra vinculado laboralmente como BARBERO en nuestra empresa, desempeñando sus funciones con responsabilidad y profesionalismo.",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            f"<br/>Fecha de expedición: {datetime.now().strftime('%d/%m/%Y')}",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "<br/><br/><br/>_________________________",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "Administrador",
            estilos["Normal"]
        )
    )

    elementos.append(
        Paragraph(
            "BarberSpringfield",
            estilos["Normal"]
        )
    )

    doc.build(elementos)

    return response


@login_required
def cierre_caja(request):
    """Reporte de cierre de caja diario: servicios realizados, ingresos y cancelaciones."""

    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect("administracion:panel_admin")

    fecha_str = request.GET.get("fecha")
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha = datetime.today().date()
    else:
        fecha = datetime.today().date()

    resumen = calcular_cierre_caja(fecha)

    return render(request, "administracion/cierre_caja.html", resumen)


@login_required
def cierre_caja_pdf(request):
    """Misma información que cierre_caja, pero descargable en PDF."""

    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect("administracion:panel_admin")

    fecha_str = request.GET.get("fecha")
    if fecha_str:
        try:
            fecha = datetime.strptime(fecha_str, "%Y-%m-%d").date()
        except ValueError:
            fecha = datetime.today().date()
    else:
        fecha = datetime.today().date()

    resumen = calcular_cierre_caja(fecha)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="cierre_caja_{fecha}.pdf"'

    doc = SimpleDocTemplate(response)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(f"Cierre de caja — {fecha.strftime('%d/%m/%Y')}", estilos["Title"]))
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"Servicios finalizados: {resumen['total_finalizadas']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Citas canceladas: {resumen['total_canceladas']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Citas sin resolver: {resumen['total_pendientes']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Total de ingresos: ${resumen['total_ingresos']:,}", estilos["Normal"]))
    elementos.append(Spacer(1, 16))

    elementos.append(Paragraph("Servicios realizados", estilos["Heading2"]))
    data_finalizadas = [["Hora", "Cliente", "Servicio", "Barbero", "Precio"]]
    for cita in resumen["finalizadas"]:
        data_finalizadas.append([
            cita.hora,
            cita.cliente.nombre,
            cita.servicio.nombre,
            cita.barbero.nombre if cita.barbero else "-",
            f"${cita.servicio.precio:,}",
        ])
    if len(data_finalizadas) == 1:
        data_finalizadas.append(["-", "Sin servicios finalizados este día", "-", "-", "-"])

    tabla_finalizadas = Table(data_finalizadas, hAlign="LEFT")
    tabla_finalizadas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#F4C542")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.black),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elementos.append(tabla_finalizadas)
    elementos.append(Spacer(1, 20))

    elementos.append(Paragraph("Citas canceladas", estilos["Heading2"]))
    data_canceladas = [["Hora", "Cliente", "Servicio", "Barbero"]]
    for cita in resumen["canceladas"]:
        data_canceladas.append([
            cita.hora,
            cita.cliente.nombre,
            cita.servicio.nombre,
            cita.barbero.nombre if cita.barbero else "-",
        ])
    if len(data_canceladas) == 1:
        data_canceladas.append(["-", "Sin cancelaciones este día", "-", "-"])

    tabla_canceladas = Table(data_canceladas, hAlign="LEFT")
    tabla_canceladas.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#3F2E22")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 9),
    ]))
    elementos.append(tabla_canceladas)

    doc.build(elementos)

    return response