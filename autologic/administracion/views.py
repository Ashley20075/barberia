from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User, Group
from citas.models import Cita, Servicio
from clientes.models import Cliente
from clientes.verificacion import enviar_correo_confirmacion
from barberos.models import Barbero
from inventario.models import Producto
from inventario.utils import registrar_movimiento
from datetime import datetime, timedelta, time
from django.db import IntegrityError, transaction
from django.core.exceptions import ValidationError
from django.http import HttpResponse
from urllib.parse import parse_qs, quote, unquote, urlparse
import re
from reportlab.platypus import SimpleDocTemplate, Paragraph, Image, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from django.conf import settings
import os
from googlecalendar.models import CuentaGoogle
from .reportes import calcular_cierre_caja
from .models import Sitio
from citas.paginacion import paginar
from notificaciones.models import Notificacion
from django.http import JsonResponse


def a_time(valor):
    """
    Convierte cualquier representación de hora a un objeto datetime.time.

    Acepta: time, datetime o str en formatos como "09:00 AM", "9:00 AM",
    "09:00", "09:00:00". Devuelve None si no se puede interpretar.
    """
    if isinstance(valor, datetime):
        return valor.time().replace(second=0, microsecond=0)

    if isinstance(valor, time):
        return valor.replace(second=0, microsecond=0)

    if isinstance(valor, str):
        texto = valor.strip().upper().replace('.', '')
        formatos = (
            '%I:%M %p',
            '%I:%M%p',
            '%I:%M:%S %p',
            '%H:%M',
            '%H:%M:%S',
        )
        for formato in formatos:
            try:
                return datetime.strptime(texto, formato).time().replace(second=0, microsecond=0)
            except ValueError:
                continue

    return None


def formatear_hora(hora):
    """Devuelve 'HH:MM' (24h) sin importar si hora es str, time o datetime."""
    h = a_time(hora)
    return h.strftime('%H:%M') if h else ''


@login_required
def panel_admin(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para acceder al panel de administración.')
        return redirect('inicio')
    
    usuarios = User.objects.all()
    clientes = Cliente.objects.all()
    grupo_barberos, _ = Group.objects.get_or_create(name='Barberos')
    # La tabla administrativa conserva perfiles activos e inactivos para poder
    # editar/reactivar sin perder el historial ni las citas asignadas.
    barberos = Barbero.objects.filter(es_barbero=True).order_by('nombre')
    # La fuente real del rol es el perfil Barbero, no cualquier grupo Django.
    barbero_emails = {email.lower() for email in Barbero.objects.filter(es_barbero=True).exclude(email='').values_list('email', flat=True)}
    cantidad_barberos = barberos.count()
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
        estado__in=["Finalizada", "Cancelada"],
        historial_archivado=False
).order_by("-fecha", "-hora")

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
        "historial_citas": paginar(historial_citas, request, parametro="pagina_historial"),
        'barberos': barberos,
        'servicios': servicios,
        'productos': productos,
        'sitio': Sitio.obtener(),
        'cantidad_barberos': cantidad_barberos,
        'barbero_emails': barbero_emails,
        "total_citas": total_citas,
        "cuenta_google": CuentaGoogle.objects.filter(usuario=request.user).first(),
        "notificaciones_no_leidas": Notificacion.objects.filter(usuario=request.user, leida=False).count(),
    }
    return render(request, 'administracion/panel_administrador.html', context)

def normalizar_mapa_google_maps(valor):
    """
    Acepta las formas más comunes de Google Maps que puede pegar el administrador:

    1. URL del iframe generado por "Compartir > Insertar un mapa".
    2. URL normal de Google Maps (maps/place, maps/search, etc.).
    3. Código HTML completo de un <iframe>.

    Google recomienda colocar la URL de incrustación en el src de un iframe.
    Si se pega una URL normal de Maps, intentamos convertirla a un mapa embebido
    usando las coordenadas o el término de búsqueda disponible en la URL.
    """
    valor = (valor or '').strip()
    if not valor:
        return ''

    # Si el administrador pega el iframe completo, extraemos únicamente src.
    match = re.search(
        r'<iframe[^>]+src=["\']([^"\']+)["\'][^>]*>',
        valor,
        flags=re.IGNORECASE,
    )
    if match:
        valor = match.group(1).strip()

    # Ya es una URL de embed. Se conserva tal cual.
    if '/maps/embed' in valor:
        return valor

    parsed = urlparse(valor)
    host = (parsed.netloc or '').lower()

    # No intentamos transformar enlaces que no sean de Google Maps.
    if 'google.' not in host and 'maps.app.goo.gl' not in host and 'goo.gl' not in host:
        return valor

    # Enlaces /maps/search/?api=1&query=... o URLs con ?q=...
    query_params = parse_qs(parsed.query)
    termino = (
        query_params.get('query', [None])[0]
        or query_params.get('q', [None])[0]
    )

    # Los enlaces /maps/place/... suelen contener las coordenadas después de @.
    coordenadas = re.search(
        r'@(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)',
        valor,
    )
    if coordenadas:
        termino = f'{coordenadas.group(1)},{coordenadas.group(2)}'

    # Si no hay query, intentamos obtener el nombre/dirección de /maps/place/...
    if not termino and '/maps/place/' in parsed.path:
        parte = parsed.path.split('/maps/place/', 1)[1].split('/')[0]
        termino = unquote(parte).replace('+', ' ')

    if termino:
        # output=embed permite mostrar el mapa directamente en un iframe.
        return f'https://www.google.com/maps?q={quote(termino)}&output=embed'

    # Los enlaces cortos maps.app.goo.gl necesitan ser resueltos por el navegador.
    # Se conserva la URL para no guardar una dirección inventada.
    return valor


@login_required
def editar_inicio(request):
    """
    Actualiza el contenido editable de la página de inicio.

    Las imágenes pueden venir de:
    1. Una URL.
    2. Un archivo seleccionado desde el dispositivo.

    Para cada imagen solamente se utiliza la fuente seleccionada.
    """

    if not request.user.is_superuser:
        messages.error(
            request,
            'No tienes permisos para realizar esta acción.'
        )
        return redirect('inicio')

    sitio = Sitio.obtener()

    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    # ============================================================
    # CAMPOS DE TEXTO
    # ============================================================

    campos = [
        'nombre_marca',
        'eslogan',
        'hero_titulo',
        'hero_descripcion',

        'servicios_titulo',
        'servicios_subtitulo',

        'barberos_titulo',
        'barberos_subtitulo',

        'nosotros_titulo',
        'nosotros_parrafo_1',
        'nosotros_parrafo_2',
        'nosotros_punto_1',
        'nosotros_punto_2',
        'nosotros_punto_3',

        'testimonios_titulo',
        'testimonios_subtitulo',
        'testimonio_1',
        'testimonio_1_autor',
        'testimonio_2',
        'testimonio_2_autor',
        'testimonio_3',
        'testimonio_3_autor',

        'cta_titulo',
        'cta_descripcion',
        'cta_boton',

        'footer_descripcion',
        'horario',
        'direccion',
        'telefono',
        'email',
        'mapa_embed_url',

        'noticias_titulo',
        'noticias_descripcion',
        'copyright_texto',
    ]

    for campo in campos:
        if campo in request.POST:
            valor = request.POST.get(campo, '').strip()
            if campo == 'mapa_embed_url':
                valor = normalizar_mapa_google_maps(valor)
            setattr(sitio, campo, valor)

    # ============================================================
    # FUNCIÓN AUXILIAR PARA IMÁGENES
    # ============================================================

    def procesar_imagen(
        fuente,
        campo_url,
        campo_archivo,
        archivo_subido
    ):
        """
        Guarda únicamente la fuente seleccionada.

        Si se selecciona URL:
        - Guarda la URL.
        - No utiliza el archivo.

        Si se selecciona archivo:
        - Guarda el archivo.
        - No utiliza la URL.
        """

        if fuente == Sitio.FUENTE_ARCHIVO:
            if archivo_subido:
                setattr(
                    sitio,
                    campo_archivo,
                    archivo_subido
                )

            setattr(
                sitio,
                campo_url,
                getattr(sitio, campo_url)
            )

        else:
            url = request.POST.get(
                campo_url,
                ''
            ).strip()

            setattr(
                sitio,
                campo_url,
                url
            )

    # ============================================================
    # IMAGEN PORTADA 1
    # ============================================================

    fuente_1 = request.POST.get(
        'hero_imagen_1_fuente',
        Sitio.FUENTE_URL
    )

    procesar_imagen(
        fuente_1,
        'hero_imagen_1_url',
        'hero_imagen_1_archivo',
        request.FILES.get('hero_imagen_1_archivo')
    )

    sitio.hero_imagen_1_fuente = fuente_1

    # ============================================================
    # IMAGEN PORTADA 2
    # ============================================================

    fuente_2 = request.POST.get(
        'hero_imagen_2_fuente',
        Sitio.FUENTE_URL
    )

    procesar_imagen(
        fuente_2,
        'hero_imagen_2_url',
        'hero_imagen_2_archivo',
        request.FILES.get('hero_imagen_2_archivo')
    )

    sitio.hero_imagen_2_fuente = fuente_2

    # ============================================================
    # IMAGEN PORTADA 3
    # ============================================================

    fuente_3 = request.POST.get(
        'hero_imagen_3_fuente',
        Sitio.FUENTE_URL
    )

    procesar_imagen(
        fuente_3,
        'hero_imagen_3_url',
        'hero_imagen_3_archivo',
        request.FILES.get('hero_imagen_3_archivo')
    )

    sitio.hero_imagen_3_fuente = fuente_3

    # ============================================================
    # IMAGEN DE "NOSOTROS"
    # ============================================================

    fuente_nosotros = request.POST.get(
        'nosotros_imagen_fuente',
        Sitio.FUENTE_URL
    )

    procesar_imagen(
        fuente_nosotros,
        'nosotros_imagen_url',
        'nosotros_imagen_archivo',
        request.FILES.get('nosotros_imagen_archivo')
    )

    sitio.nosotros_imagen_fuente = fuente_nosotros

    # ============================================================
    # IMAGEN DE FACHADA (EXTERIOR DE LA BARBERÍA)
    # ============================================================

    fuente_fachada = request.POST.get(
        'fachada_imagen_fuente',
        Sitio.FUENTE_URL
    )

    procesar_imagen(
        fuente_fachada,
        'fachada_imagen_url',
        'fachada_imagen_archivo',
        request.FILES.get('fachada_imagen_archivo')
    )

    sitio.fachada_imagen_fuente = fuente_fachada

    # ============================================================
    # GUARDAR
    # ============================================================

    try:
        sitio.full_clean()
        sitio.save()

        messages.success(
            request,
            '✅ La información de la página de inicio fue actualizada correctamente.'
        )

    except ValidationError as e:
        if e.messages:
            messages.error(
                request,
                f'❌ No se pudo guardar la información: {e.messages[0]}'
            )
        else:
            messages.error(
                request,
                '❌ No se pudo guardar la información.'
            )

    return redirect('administracion:panel_admin')


@login_required
def asignar_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    user = get_object_or_404(User, id=id)
    cliente = Cliente.objects.filter(user=user).first()
    cedula = (request.POST.get('cedula') or (cliente.cedula if cliente else '') or '').strip()
    telefono = (request.POST.get('telefono') or (cliente.telefono if cliente else '') or '').strip()
    especialidad = (request.POST.get('especialidad') or 'General').strip() or 'General'

    if not user.email:
        messages.error(request, 'No se puede asignar el rol de barbero porque la cuenta no tiene correo electrónico.')
        return redirect('administracion:panel_admin')
    if not cedula:
        messages.error(request, 'Ingresa la cédula para convertir esta cuenta en barbero.')
        return redirect('administracion:panel_admin')

    try:
        with transaction.atomic():
            barbero = Barbero.objects.filter(email__iexact=user.email).first()
            if Barbero.objects.filter(cedula=cedula).exclude(pk=barbero.pk if barbero else None).exists():
                messages.error(request, 'Esa cédula ya está registrada en otro barbero.')
                return redirect('administracion:panel_admin')
            if Cliente.objects.filter(cedula=cedula).exclude(user=user).exists():
                messages.error(request, 'Esa cédula ya está asociada a otro cliente.')
                return redirect('administracion:panel_admin')

            nombre = ((cliente.nombre.strip() if cliente else '') or user.get_full_name().strip() or user.username)
            if barbero:
                # Si ya existía un perfil inactivo, se reactiva y sincroniza; no se duplica.
                barbero.nombre = nombre
                barbero.cedula = cedula
                barbero.telefono = telefono or barbero.telefono
                barbero.especialidad = especialidad
                barbero.activo = True
                barbero.es_barbero = True
                barbero.save()
            else:
                Barbero.objects.create(
                    nombre=nombre, cedula=cedula, telefono=telefono,
                    email=user.email, especialidad=especialidad, activo=True,
                    jornada_inicio='08:00', jornada_fin='18:00', duracion_cita=30,
                    dias_laborales='LUN,MAR,MIE,JUE,VIE,SAB', dia_descanso='DOM',
                    tiempo_entre_citas=15,
                )

            grupo, _ = Group.objects.get_or_create(name='Barberos')
            user.groups.add(grupo)
            if cliente:
                cambios = False
                if cliente.cedula != cedula:
                    cliente.cedula = cedula
                    cambios = True
                if telefono and cliente.telefono != telefono:
                    cliente.telefono = telefono
                    cambios = True
                if cambios:
                    cliente.save()
        messages.success(request, f'¡Listo! {user.username} aparece en la tabla de barberos y puede ingresar como barbero.')
    except IntegrityError:
        messages.error(request, 'No se pudo asignar el rol: la cédula ya está registrada en otro perfil.')
    except Exception as exc:
        messages.error(request, f'No se pudo convertir la cuenta en barbero: {exc}')
    return redirect('administracion:panel_admin')

@login_required
def quitar_barbero(request, id):
    """Quita el rol de barbero al usuario sin borrar la cuenta ni las citas."""
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    usuario = get_object_or_404(User, id=id)
    perfil = Barbero.objects.filter(email__iexact=usuario.email, es_barbero=True).first()
    if perfil is None:
        messages.error(request, 'Este usuario no tiene actualmente el rol de barbero.')
        return redirect('administracion:panel_admin')

    with transaction.atomic():
        perfil.es_barbero = False
        perfil.activo = False
        perfil.save(update_fields=['es_barbero', 'activo'])
        grupo = Group.objects.filter(name='Barberos').first()
        if grupo:
            usuario.groups.remove(grupo)

    # La cuenta sigue activa y puede continuar usando el sistema como cliente.
    messages.success(
        request,
        f'El rol de barbero de "{perfil.nombre}" fue retirado. Su cuenta y sus citas anteriores se conservaron.'
    )
    return redirect('administracion:panel_admin')

@login_required
def desactivar_usuario(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    usuario = get_object_or_404(User, id=id)
    usuario.is_active = False
    usuario.save(update_fields=['is_active'])
    # Ocultarlo de la tabla operativa de barberos sin borrar sus datos ni citas.
    Barbero.objects.filter(email__iexact=usuario.email).update(activo=False)
    messages.success(request, f'✅ El usuario "{usuario.username}" fue desactivado. Su perfil permanece en la tabla administrativa como inactivo y sus citas se conservan.')
    return redirect('administracion:panel_admin')

@login_required
def activar_usuario(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    
    usuario = get_object_or_404(User, id=id)

    # Una cuenta creada por el administrador y pendiente de verificación
    # NO puede activarse manualmente. Debe abrir primero el enlace enviado
    # al correo; ese enlace es el que confirma que la dirección existe.
    cliente = Cliente.objects.filter(user=usuario).first()
    perfil_barbero = Barbero.objects.filter(email__iexact=usuario.email, es_barbero=True).first()
    if cliente is not None and not cliente.correo_confirmado and perfil_barbero is None:
        messages.error(
            request,
            f'⚠️ El usuario "{usuario.username}" todavía no ha confirmado su correo. '
            'Debe abrir el enlace recibido antes de poder activar la cuenta.'
        )
        return redirect('administracion:panel_admin')

    usuario.is_active = True
    usuario.save(update_fields=['is_active'])
    # Al reactivar la cuenta, recuperar también su perfil de barbero si existe.
    Barbero.objects.filter(email__iexact=usuario.email, es_barbero=True).update(activo=True)
    messages.success(request, f'✅ El usuario "{usuario.username}" fue activado.')
    return redirect('administracion:panel_admin')

@login_required
def crear_usuario(request):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')

    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    nombre = request.POST.get('nombre', '').strip()
    apellido = request.POST.get('apellido', '').strip()
    cedula = request.POST.get('cedula', '').strip()
    telefono = request.POST.get('telefono', '').strip()
    email = request.POST.get('email', '').strip().lower()
    password = request.POST.get('password', '')
    confirm_password = request.POST.get('confirm_password', '')

    if not all([nombre, apellido, cedula, telefono, email, password]):
        messages.error(request, 'Completa todos los campos obligatorios.')
        return redirect('administracion:panel_admin')
    if password != confirm_password:
        messages.error(request, '❌ Las contraseñas no coinciden.')
        return redirect('administracion:panel_admin')
    usuario_existente = User.objects.filter(email__iexact=email).first()
    if usuario_existente is None:
        usuario_existente = User.objects.filter(username__iexact=email).first()
    if usuario_existente is not None:
        cliente_existente = Cliente.objects.filter(user=usuario_existente).first()
        if cliente_existente is not None and not cliente_existente.correo_confirmado and not usuario_existente.is_active:
            enviado = enviar_correo_confirmacion(request, usuario_existente)
            if enviado:
                messages.success(
                    request,
                    f'La cuenta de {usuario_existente.get_full_name() or usuario_existente.username} ya estaba creada. '
                    f'Reenviamos el enlace de confirmación a {usuario_existente.email}.'
                )
            else:
                messages.success(request, 'La cuenta ya estaba creada y continúa pendiente de confirmación.')
                messages.warning(request, 'No pudimos reenviar el correo. Revisa la conexión SMTP e inténtalo de nuevo.')
        else:
            messages.error(request, '❌ Este correo ya está asociado a una cuenta activa.')
        return redirect('administracion:panel_admin')
    if Cliente.objects.filter(cedula=cedula).exists():
        messages.error(request, '❌ La cédula ya está registrada.')
        return redirect('administracion:panel_admin')

    try:
        with transaction.atomic():
            user = User.objects.create_user(
                username=email,
                email=email,
                password=password,
                first_name=nombre,
                last_name=apellido,
                is_active=False,
            )
            Cliente.objects.create(
                user=user,
                nombre=f'{nombre} {apellido}',
                cedula=cedula,
                telefono=telefono,
                email=email,
                correo_confirmado=False,
            )
    except IntegrityError:
        messages.error(request, '❌ Ya existe una cuenta con ese correo o esa cédula.')
        return redirect('administracion:panel_admin')
    except Exception:
        messages.error(request, '❌ No se pudo crear el usuario. Inténtalo de nuevo.')
        return redirect('administracion:panel_admin')

    # La cuenta ya quedó creada y guardada. El correo se envía después,
    # sin revertir la cuenta si Gmail tiene una caída o rechaza el envío.
    enviado = enviar_correo_confirmacion(request, user)
    if enviado:
        messages.success(
            request,
            f'✅ ¡Cuenta creada con éxito! {nombre} {apellido} ya está registrado. '
            f'Enviamos el enlace de confirmación a {email}.'
        )
    else:
        messages.success(
            request,
            f'✅ ¡Cuenta creada con éxito! {nombre} {apellido} ya está registrado. '
            'La cuenta quedó pendiente de confirmar el correo.'
        )
        messages.warning(
            request,
            f'No pudimos enviar el correo a {email}. Revisa el SMTP y vuelve a enviar la confirmación.'
        )
    return redirect('administracion:panel_admin')

@login_required
def editar_cita(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')

    cita = get_object_or_404(Cita, id=id)

    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    cliente_id = request.POST.get('cliente')
    servicio_id = request.POST.get('servicio')
    barbero_id = request.POST.get('barbero')
    fecha = request.POST.get('fecha')
    hora_raw = request.POST.get('hora')

    # La hora llega del selector como "HH:MM" (24h). En la base de datos
    # la hora de la cita se guarda como texto "09:00 AM", igual que al
    # agendar, así que la convertimos a ese formato.
    if hora_raw:
        hora_obj = a_time(hora_raw)
        if hora_obj is None:
            messages.error(
                request,
                '❌ La hora seleccionada no tiene un formato válido.'
            )
            return redirect('administracion:panel_admin')
        hora_str = hora_obj.strftime('%I:%M %p')
    else:
        # Si no se envió hora, se conserva la que ya tenía la cita.
        hora_str = cita.hora

    estado = request.POST.get('estado')

    estados_validos = {
        "Pendiente",
        "Confirmada",
        "Cancelada",
        "Finalizada",
    }

    if estado not in estados_validos:
        messages.error(
            request,
            "❌ El estado seleccionado no es válido."
        )
        return redirect('administracion:panel_admin')

    cliente = get_object_or_404(Cliente, id=cliente_id)
    servicio = get_object_or_404(Servicio, id=servicio_id)
    barbero = get_object_or_404(Barbero, id=barbero_id)

    try:
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    except (TypeError, ValueError):
        messages.error(request, '❌ La fecha seleccionada no es válida.')
        return redirect('administracion:panel_admin')

    if not barbero.es_dia_laboral(fecha_obj):
        messages.error(request, f'❌ {barbero.nombre} no trabaja en esa fecha.')
        return redirect('administracion:panel_admin')

    if barbero.es_dia_descanso(fecha_obj):
        messages.error(request, f'❌ {barbero.nombre} tiene descanso en esa fecha.')
        return redirect('administracion:panel_admin')

    cita_existente = Cita.objects.filter(
        barbero=barbero,
        fecha=fecha_obj,
        hora=hora_str
    ).exclude(id=id).exclude(estado='Cancelada').exists()

    if cita_existente:
        messages.error(request, '❌ El barbero ya tiene una cita en ese horario.')
        return redirect('administracion:panel_admin')

    cita.cliente = cliente
    cita.servicio = servicio
    cita.barbero = barbero
    cita.fecha = fecha_obj
    cita.hora = hora_str
    cita.estado = estado
    cita.save()
    # La sincronización con Google Calendar (incluida la reasignación
    # de barbero) la hace automáticamente la señal post_save.

    messages.success(request, '✅ Cita actualizada correctamente.')
    return redirect('administracion:panel_admin')

@login_required
def horarios_disponibles_editar(request):
    if not request.user.is_superuser:
        return JsonResponse(
            {'error': 'No tienes permisos para realizar esta acción.'},
            status=403
        )

    barbero_id = request.GET.get('barbero_id')
    fecha = request.GET.get('fecha')
    servicio_id = request.GET.get('servicio_id')
    cita_id = request.GET.get('cita_id')

    if not barbero_id or not fecha or not servicio_id:
        return JsonResponse({
            'horarios': []
        })

    try:
        barbero = Barbero.objects.get(id=barbero_id, activo=True, es_barbero=True)
        servicio = Servicio.objects.get(id=servicio_id)
        fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
    except (Barbero.DoesNotExist, Servicio.DoesNotExist, ValueError):
        return JsonResponse({
            'horarios': []
        })

    # Verificar si el barbero trabaja ese día
    if not barbero.es_dia_laboral(fecha_obj):
        return JsonResponse({
            'horarios': [],
            'mensaje': f'{barbero.nombre} no trabaja en esa fecha.'
        })

    # Verificar día de descanso
    if barbero.es_dia_descanso(fecha_obj):
        return JsonResponse({
            'horarios': [],
            'mensaje': f'{barbero.nombre} tiene descanso en esa fecha.'
        })

    # Duración del servicio
    duracion = servicio.duracion or 35

    # Obtener horarios disponibles usando la lógica existente del barbero.
    # Pueden venir como texto ("09:00 AM") o como objetos time, así que
    # todo se normaliza a time antes de seguir.
    horarios_originales = list(
        barbero.horarios_disponibles(
            fecha_obj,
            duracion=duracion
        ) or []
    )

    horas = {}
    for h in horarios_originales:
        h_time = a_time(h)
        if h_time is not None:
            horas[h_time] = True

    # Si estamos editando una cita existente,
    # no debemos bloquear su propia hora.
    cita_actual = None

    if cita_id:
        try:
            cita_actual = Cita.objects.get(id=cita_id)
        except (Cita.DoesNotExist, ValueError):
            cita_actual = None

    if (
        cita_actual
        and cita_actual.barbero_id == barbero.id
        and str(cita_actual.fecha) == str(fecha_obj)
        and cita_actual.hora
    ):
        hora_cita = a_time(cita_actual.hora)
        if hora_cita is not None:
            horas[hora_cita] = True

    # Ordenar las horas y convertir a formato visible
    horarios_formateados = []

    for hora in sorted(horas.keys()):
        horarios_formateados.append({
            'value': hora.strftime('%H:%M'),
            'label': hora.strftime('%I:%M %p').lstrip('0')
        })

    return JsonResponse({
        'horarios': horarios_formateados
    })

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
            
            dias_validos = {codigo for codigo, _ in Barbero.DIAS_SEMANA}
            dia_descanso = request.POST.get('dia_descanso', 'DOM').strip().upper()
            if dia_descanso not in dias_validos:
                raise ValueError('Selecciona un día de descanso válido.')
            dias_seleccionados = [
                codigo for codigo, _ in Barbero.DIAS_SEMANA
                if codigo != dia_descanso
            ]

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
                dias_laborales=','.join(dias_seleccionados),
                dia_descanso=dia_descanso,
                tiempo_entre_citas=int(request.POST.get('tiempo_entre_citas', 15)),
                imagen_url=request.POST.get('imagen_url', '').strip(),
                calificacion=request.POST.get('calificacion', '5.0') or '5.0',
                numero_resenas=int(request.POST.get('numero_resenas', 0) or 0),
                instagram=request.POST.get('instagram', '').strip(),
                facebook=request.POST.get('facebook', '').strip(),
                whatsapp=request.POST.get('whatsapp', '').strip()
            )
            # Si el correo ya pertenece a una cuenta, vincular automáticamente
            # esa cuenta con el rol de barbero para que pueda iniciar sesión.
            usuario = User.objects.filter(email__iexact=barbero.email).first()
            if usuario:
                grupo, _ = Group.objects.get_or_create(name='Barberos')
                usuario.groups.add(grupo)
            messages.success(request, f'✅ Barbero "{barbero.nombre}" agregado correctamente.' + (
                ' Su cuenta de usuario quedó vinculada.' if usuario else
                ' Para iniciar sesión necesitará una cuenta de usuario con ese correo.'
            ))
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
            barbero.imagen_url = request.POST.get('imagen_url', '').strip()
            barbero.calificacion = request.POST.get('calificacion', '5.0') or '5.0'
            barbero.numero_resenas = int(request.POST.get('numero_resenas', 0) or 0)
            barbero.instagram = request.POST.get('instagram', '').strip()
            barbero.facebook = request.POST.get('facebook', '').strip()
            barbero.whatsapp = request.POST.get('whatsapp', '').strip()
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
            
            dias_validos = {codigo for codigo, _ in Barbero.DIAS_SEMANA}
            dia_descanso = request.POST.get('dia_descanso', 'DOM').strip().upper()
            if dia_descanso not in dias_validos:
                raise ValueError('Selecciona un día de descanso válido.')
            barbero.dia_descanso = dia_descanso
            barbero.dias_laborales = ','.join(
                codigo for codigo, _ in Barbero.DIAS_SEMANA
                if codigo != dia_descanso
            )
            
            barbero.save()
            messages.success(request, f'✅ Barbero "{barbero.nombre}" actualizado correctamente.')
            
        except IntegrityError:
            messages.error(
                request,
                '❌ Ese correo o esa cédula ya están en uso por otro barbero.'
            )

        except ValueError as error:
            messages.error(request, f'❌ {error}')

        except Exception:
            messages.error(request, '❌ No se pudo actualizar el barbero. Intentá de nuevo.')
        
        return redirect('administracion:panel_admin')
    
    return redirect('administracion:panel_admin')

@login_required
def cambiar_estado_barbero(request, id):
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    if request.method != 'POST':
        return redirect('administracion:panel_admin')
    barbero = get_object_or_404(Barbero, id=id, es_barbero=True)
    usuario = User.objects.filter(email__iexact=barbero.email).first()
    activar = not barbero.activo
    barbero.activo = activar
    barbero.save(update_fields=['activo'])
    if usuario:
        usuario.is_active = activar
        usuario.save(update_fields=['is_active'])
        grupo, _ = Group.objects.get_or_create(name='Barberos')
        usuario.groups.add(grupo)
    estado = 'reactivado' if activar else 'desactivado'
    messages.success(request, f'El barbero {barbero.nombre} fue {estado}. Sus citas e historial permanecen guardados.')
    return redirect('administracion:panel_admin')


@login_required
def eliminar_barbero(request, id):
    """Eliminación lógica de la cuenta del barbero: bloquea acceso y retira el rol,
    pero conserva el usuario, el perfil histórico y todas las citas relacionadas.
    No se usa User.delete() porque podría borrar en cascada el perfil de cliente y sus citas.
    """
    if not request.user.is_superuser:
        messages.error(request, 'No tienes permisos para realizar esta acción.')
        return redirect('administracion:panel_admin')
    if request.method != 'POST':
        return redirect('administracion:panel_admin')

    perfil = get_object_or_404(Barbero, id=id, es_barbero=True)
    usuario = User.objects.filter(email__iexact=perfil.email).first()
    with transaction.atomic():
        perfil.es_barbero = False
        perfil.activo = False
        perfil.save(update_fields=['es_barbero', 'activo'])
        if usuario:
            usuario.is_active = False
            usuario.save(update_fields=['is_active'])
            grupo = Group.objects.filter(name='Barberos').first()
            if grupo:
                usuario.groups.remove(grupo)

    messages.success(
        request,
        f'La cuenta de "{perfil.nombre}" fue retirada del sistema. Se bloqueó su acceso y se conservaron las citas y el historial.'
    )
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
        try:
            nuevo_stock = int(request.POST.get('stock'))
        except (TypeError, ValueError):
            messages.error(request, '❌ El stock debe ser un número entero.')
            return redirect('administracion:panel_admin')

        stock_cambio = nuevo_stock != producto.stock_actual

        if stock_cambio and not (5 <= nuevo_stock <= 20):
            messages.error(request, '❌ El stock debe estar entre 5 y 20 unidades.')
            return redirect('administracion:panel_admin')

        producto.nombre = request.POST.get('nombre')
        producto.precio_unitario = request.POST.get('precio')
        if not stock_cambio:
            producto.stock_actual = nuevo_stock

        try:
            producto.full_clean(exclude=['stock_actual'] if stock_cambio else None)
            producto.save()

            # Si cambió el stock se registra como AJUSTE, para que el cambio
            # aparezca en el historial de movimientos de inventario.
            if stock_cambio:
                registrar_movimiento(
                    producto=producto,
                    tipo='AJUSTE',
                    cantidad=nuevo_stock,
                    usuario=request.user,
                    nota='Ajuste manual desde el panel de administración',
                )

            messages.success(request, '✅ Producto actualizado correctamente.')

        except ValidationError as e:
            messages.error(request, e.messages[0])

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


def _parsear_rango_cierre_caja(request):
    """
    Lee fecha_inicio/fecha_fin (y opcionalmente hora_inicio/hora_fin) de
    la querystring. Mantiene compatibilidad con el parámetro viejo
    `fecha` (un solo día). Si algo falta o es inválido, cae a "hoy".
    """

    hoy = datetime.today().date()

    fecha_inicio_str = request.GET.get("fecha_inicio") or request.GET.get("fecha")
    fecha_fin_str = request.GET.get("fecha_fin") or request.GET.get("fecha")

    try:
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date() if fecha_inicio_str else hoy
    except ValueError:
        fecha_inicio = hoy

    try:
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date() if fecha_fin_str else hoy
    except ValueError:
        fecha_fin = hoy

    # Si el usuario invierte las fechas, las corregimos en vez de devolver vacío.
    if fecha_fin < fecha_inicio:
        fecha_inicio, fecha_fin = fecha_fin, fecha_inicio

    hora_inicio = (request.GET.get("hora_inicio") or "").strip() or None
    hora_fin = (request.GET.get("hora_fin") or "").strip() or None
    if hora_inicio and hora_fin and hora_fin < hora_inicio:
        hora_inicio, hora_fin = hora_fin, hora_inicio

    return fecha_inicio, fecha_fin, hora_inicio, hora_fin


@login_required
def cierre_caja(request):
    """Reporte de cierre de caja: servicios realizados, ingresos y cancelaciones en un rango de fecha/hora."""

    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect("administracion:panel_admin")

    fecha_inicio, fecha_fin, hora_inicio, hora_fin = _parsear_rango_cierre_caja(request)

    resumen = calcular_cierre_caja(fecha_inicio, fecha_fin, hora_inicio, hora_fin)

    return render(request, "administracion/cierre_caja.html", resumen)


@login_required
def cierre_caja_pdf(request):
    """Misma información que cierre_caja, pero descargable en PDF."""

    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para ver esta página.")
        return redirect("administracion:panel_admin")

    fecha_inicio, fecha_fin, hora_inicio, hora_fin = _parsear_rango_cierre_caja(request)

    resumen = calcular_cierre_caja(fecha_inicio, fecha_fin, hora_inicio, hora_fin)

    if fecha_inicio == fecha_fin:
        titulo_periodo = fecha_inicio.strftime("%d/%m/%Y")
        nombre_archivo = f"{fecha_inicio}"
    else:
        titulo_periodo = f"{fecha_inicio.strftime('%d/%m/%Y')} — {fecha_fin.strftime('%d/%m/%Y')}"
        nombre_archivo = f"{fecha_inicio}_a_{fecha_fin}"

    if hora_inicio and hora_fin:
        titulo_periodo += f" · {hora_inicio} a {hora_fin}"

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="cierre_caja_{nombre_archivo}.pdf"'

    doc = SimpleDocTemplate(response)
    estilos = getSampleStyleSheet()
    elementos = []

    elementos.append(Paragraph(f"Cierre de caja — {titulo_periodo}", estilos["Title"]))
    elementos.append(Spacer(1, 10))
    elementos.append(Paragraph(f"Servicios finalizados: {resumen['total_finalizadas']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Citas canceladas: {resumen['total_canceladas']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Citas sin resolver: {resumen['total_pendientes']}", estilos["Normal"]))
    elementos.append(Paragraph(f"Total de ingresos: ${resumen['total_ingresos']:,}", estilos["Normal"]))
    elementos.append(Spacer(1, 16))

    elementos.append(Paragraph("Servicios realizados", estilos["Heading2"]))
    if resumen["es_rango"]:
        encabezado_finalizadas = ["Fecha", "Hora", "Cliente", "Servicio", "Barbero", "Precio"]
    else:
        encabezado_finalizadas = ["Hora", "Cliente", "Servicio", "Barbero", "Precio"]
    data_finalizadas = [encabezado_finalizadas]
    for cita in resumen["finalizadas"]:
        fila = []
        if resumen["es_rango"]:
            fila.append(cita.fecha.strftime("%d/%m/%Y"))
        fila += [
            cita.hora,
            cita.cliente.nombre,
            cita.servicio.nombre,
            cita.barbero.nombre if cita.barbero else "-",
            f"${cita.servicio.precio:,}",
        ]
        data_finalizadas.append(fila)
    if len(data_finalizadas) == 1:
        fila_vacia = ["Sin servicios finalizados en este período"] + ["-"] * (len(encabezado_finalizadas) - 1)
        data_finalizadas.append(fila_vacia)

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
    if resumen["es_rango"]:
        encabezado_canceladas = ["Fecha", "Hora", "Cliente", "Servicio", "Barbero"]
    else:
        encabezado_canceladas = ["Hora", "Cliente", "Servicio", "Barbero"]
    data_canceladas = [encabezado_canceladas]
    for cita in resumen["canceladas"]:
        fila = []
        if resumen["es_rango"]:
            fila.append(cita.fecha.strftime("%d/%m/%Y"))
        fila += [
            cita.hora,
            cita.cliente.nombre,
            cita.servicio.nombre,
            cita.barbero.nombre if cita.barbero else "-",
        ]
        data_canceladas.append(fila)
    if len(data_canceladas) == 1:
        fila_vacia = ["Sin cancelaciones en este período"] + ["-"] * (len(encabezado_canceladas) - 1)
        data_canceladas.append(fila_vacia)

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

@login_required
def vaciar_historial_admin(request):

    if not request.user.is_superuser:
        messages.error(
            request,
            "No tienes permisos para realizar esta acción."
        )
        return redirect("inicio")

    if request.method == "POST":

        Cita.objects.filter(
            estado__in=["Finalizada", "Cancelada"]
        ).update(
            historial_archivado=True
        )

        messages.success(
            request,
            "✅ El historial de citas ha sido vaciado correctamente."
        )

    return redirect("administracion:panel_admin")


@login_required
def agendar_cita_admin(request):
    """
    El administrador agenda una cita a nombre de un cliente.

    Cubre el caso de alguien que llega a la barbería sin cuenta en la
    página: en vez de obligarlo a registrarse, el admin carga su
    nombre y teléfono ahí mismo (se crea un Cliente sin usuario
    asociado, solo para dejar constancia) y agenda su turno igual que
    a cualquier otro cliente. Reutiliza las mismas reglas que ya
    valía el agendamiento del cliente (día laboral, día de descanso,
    solapamiento de horarios), para que una cita creada desde acá no
    rompa la agenda del barbero.
    """
    if not request.user.is_superuser:
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect("inicio")

    if request.method == "POST":
        adicionales = request.POST.getlist("adicionales")
        adicionales_str = ", ".join(adicionales) if adicionales else "Ninguno"

        tipo_cliente = request.POST.get("tipo_cliente", "registrado")

        # -------------------------------------------------- Cliente
        if tipo_cliente == "nuevo":
            nombre_nuevo = (request.POST.get("cliente_nuevo_nombre") or "").strip()
            telefono_nuevo = (request.POST.get("cliente_nuevo_telefono") or "").strip()
            cedula_nueva = (request.POST.get("cliente_nuevo_cedula") or "").strip() or None

            if not nombre_nuevo:
                messages.error(request, "❌ Escribí el nombre del cliente.")
                return redirect("administracion:agendar_cita_admin")

            if cedula_nueva and Cliente.objects.filter(cedula=cedula_nueva).exists():
                messages.error(request, "❌ Ya hay un cliente registrado con esa cédula.")
                return redirect("administracion:agendar_cita_admin")

            cliente = Cliente.objects.create(
                user=None,
                nombre=nombre_nuevo,
                telefono=telefono_nuevo or None,
                cedula=cedula_nueva,
            )
        else:
            try:
                cliente = Cliente.objects.get(id=request.POST.get("cliente"))
            except (Cliente.DoesNotExist, ValueError, TypeError):
                messages.error(request, "❌ Elegí un cliente válido.")
                return redirect("administracion:agendar_cita_admin")

        # -------------------------------------------------- Resto de datos
        try:
            barbero = Barbero.objects.get(id=request.POST.get("barbero"), activo=True, es_barbero=True)
            servicio = Servicio.objects.get(id=request.POST.get("servicio"))
            duracion_total = int(request.POST.get("duracion_total", 40))
            fecha = request.POST.get("fecha")
            hora = request.POST.get("hora")
            datetime.strptime(hora, "%I:%M %p")
        except (Barbero.DoesNotExist, Servicio.DoesNotExist, ValueError, TypeError):
            messages.error(request, "❌ Datos inválidos al agendar la cita.")
            return redirect("administracion:agendar_cita_admin")

        fecha_obj = datetime.strptime(fecha, "%Y-%m-%d").date()

        if not barbero.es_dia_laboral(fecha_obj) or barbero.es_dia_descanso(fecha_obj):
            messages.error(request, f"❌ {barbero.nombre} no trabaja ese día.")
            return redirect("administracion:agendar_cita_admin")

        if Cita.objects.filter(cliente=cliente, fecha=fecha,
                                estado__in=["Pendiente", "Confirmada"]).exists():
            messages.error(request, "❌ Ese cliente ya tiene una cita ese día.")
            return redirect("administracion:agendar_cita_admin")

        inicio_nueva = datetime.strptime(hora, "%I:%M %p")
        fin_nueva = inicio_nueva + timedelta(minutes=duracion_total)

        for cita in Cita.objects.filter(barbero=barbero, fecha=fecha,
                                         estado__in=["Pendiente", "Confirmada"]):
            inicio = datetime.strptime(cita.hora, "%I:%M %p")
            fin = inicio + timedelta(minutes=cita.duracion_total or 40)
            if inicio_nueva < fin and fin_nueva > inicio:
                messages.error(request, "❌ Ese horario se cruza con otra cita del barbero.")
                return redirect("administracion:agendar_cita_admin")

        with transaction.atomic():
            Cita.objects.create(
                cliente=cliente,
                servicio=servicio,
                barbero=barbero,
                adicionales=adicionales_str,
                productos="Ninguno",
                fecha=fecha,
                hora=hora,
                duracion_total=duracion_total,
                estado="Pendiente",
            )

        messages.success(
            request,
            f"✅ Cita agendada para {cliente.nombre} con {barbero.nombre}."
        )
        return redirect("administracion:panel_admin")

    return render(request, "administracion/agendar_cita.html", {
        # Antes esto listaba TODOS los Cliente, incluidos los que
        # ademas son barberos o administradores (alguien puede haberse
        # registrado como cliente antes de pasar a formar parte del
        # equipo). Se excluyen los correos que ya pertenecen a un
        # barbero o a un superusuario, para que el desplegable solo
        # muestre clientes de verdad.
        "clientes": Cliente.objects.exclude(
            email__in=Barbero.objects.filter(es_barbero=True).values_list("email", flat=True)
        ).exclude(
            user__is_staff=True
        ).exclude(
            user__is_superuser=True
        ).order_by("nombre"),
        "barberos": Barbero.objects.filter(activo=True, es_barbero=True).order_by("nombre"),
        "servicios": Servicio.objects.all().order_by("id"),
    })