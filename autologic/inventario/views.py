from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models, transaction
from django.db.models import Sum
from django.utils import timezone
from .models import Producto, MovimientoInventario
from .forms import ProductoForm, MovimientoForm
from .utils import registrar_movimiento
from django.http import HttpResponse
from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph
)
from datetime import datetime 
import os

from reportlab.platypus import Image
from django.conf import settings


from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet

@login_required
def dashboard_inventario(request):
    """Vista principal del inventario con estadísticas"""
    productos = Producto.objects.filter(activo=True).order_by('nombre')
    total_productos = productos.count()
    productos_bajo_stock = productos.filter(stock_actual__lte=models.F('stock_minimo')).count()
    ultimos_movimientos = MovimientoInventario.objects.select_related('producto', 'usuario').order_by('-fecha')[:20]  # <-- Más movimientos
    stock_total = productos.aggregate(total=Sum('stock_actual'))['total'] or 0
    
    context = {
        'productos': productos,
        'total_productos': total_productos,
        'productos_bajo_stock': productos_bajo_stock,
        'stock_total': stock_total,
        'ultimos_movimientos': ultimos_movimientos,
    }
    return render(request, 'inventario/dashboard.html', context)

@login_required
def agregar_producto(request):
    if request.method == 'POST':
        form = ProductoForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                inicial = form.cleaned_data.get('stock_actual') or 0
                producto = form.save(commit=False)
                producto.stock_actual = 0
                producto.save()
                if inicial > 0:
                    # El stock inicial también queda en el historial.
                    registrar_movimiento(
                        producto, 'ENTRADA', inicial, usuario=request.user,
                        nota='Stock inicial al crear el producto',
                    )
            messages.success(request, f'✅ Producto "{producto.nombre}" agregado exitosamente.')
            return redirect('inventario:dashboard')
        for campo, errores in form.errors.items():
            for error in errores:
                messages.error(request, f'❌ {error}')
    else:
        form = ProductoForm()
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Agregar Producto'})

@login_required
def editar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        form = ProductoForm(request.POST, instance=producto)
        if form.is_valid():
            form.save()
            messages.success(request, f'✅ Producto "{producto.nombre}" actualizado correctamente.')
            return redirect('inventario:dashboard')
    else:
        form = ProductoForm(instance=producto)
    return render(request, 'inventario/producto_form.html', {'form': form, 'titulo': 'Editar Producto'})

@login_required
def movimiento_inventario(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    
    if request.method == 'POST':
        form = MovimientoForm(request.POST)
        if form.is_valid():
            datos = form.cleaned_data

            try:
                movimiento = registrar_movimiento(
                    producto=producto,
                    tipo=datos['tipo'],
                    cantidad=datos['cantidad'],
                    usuario=request.user,
                    proveedor=datos.get('proveedor') if datos['tipo'] == 'ENTRADA' else None,
                    nota=datos.get('nota'),
                )
            except ValueError as e:
                messages.error(request, f'❌ {e}')
                return redirect('inventario:dashboard')

            # Respeta la fecha indicada en el formulario
            if datos.get('fecha'):
                movimiento.fecha = datos['fecha']
                movimiento.save(update_fields=['fecha'])

            etiquetas = {
                'ENTRADA': f'✅ Entrada registrada. Nuevo stock: {producto.stock_actual}',
                'SALIDA': f'✅ Salida registrada. Stock: {producto.stock_actual}',
                'AJUSTE': f'✅ Ajuste realizado. Nuevo stock: {producto.stock_actual}',
            }
            messages.success(request, etiquetas[datos['tipo']])
            return redirect('inventario:dashboard')
        else:
            # El formulario trae errores: se muestran en vez de perderse
            for campo, errores in form.errors.items():
                for error in errores:
                    messages.error(request, f'❌ {error}')
            return redirect('inventario:dashboard')
    else:
        form = MovimientoForm(initial={'fecha': timezone.now()})  # <-- Fecha por defecto
    
    return render(request, 'inventario/movimiento_form.html', {
        'form': form,
        'producto': producto
    })

@login_required
def eliminar_producto(request, producto_id):
    producto = get_object_or_404(Producto, id=producto_id)
    if request.method == 'POST':
        nombre = producto.nombre
        producto.delete()
        messages.success(request, f'✅ Producto "{nombre}" eliminado correctamente.')
        return redirect('inventario:dashboard')
    return render(request, 'inventario/eliminar_confirm.html', {'producto': producto})

# ========== NUEVA VISTA: HISTORIAL COMPLETO ==========
@login_required
def historial_movimientos(request):
    movimientos = MovimientoInventario.objects.select_related('producto', 'usuario').order_by('-fecha')
    
    # Filtros
    tipo = request.GET.get('tipo')
    producto_id = request.GET.get('producto')
    fecha_inicio = request.GET.get('fecha_inicio')
    fecha_fin = request.GET.get('fecha_fin')
    
    if tipo:
        movimientos = movimientos.filter(tipo=tipo)
    if producto_id:
        movimientos = movimientos.filter(producto_id=producto_id)
    if fecha_inicio:
        movimientos = movimientos.filter(fecha__date__gte=fecha_inicio)
    if fecha_fin:
        movimientos = movimientos.filter(fecha__date__lte=fecha_fin)
    
    productos = Producto.objects.filter(activo=True)
    
    context = {
        'movimientos': movimientos,
        'productos': productos,
        'tipos': MovimientoInventario.TIPO_MOVIMIENTO,
    }
    return render(request, 'inventario/historial_movimientos.html', context)

@login_required
def reporte_inventario_pdf(request):
    """PDF de inventario con la identidad visual del sitio (dorado/negro/crema)."""
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.units import cm
    from reportlab.lib.styles import ParagraphStyle
    from reportlab.lib.enums import TA_CENTER

    ORO = colors.HexColor('#d4a017')
    NEGRO = colors.HexColor('#1a1410')
    CREMA = colors.HexColor('#faf5ea')
    BORDE = colors.HexColor('#e3d7bd')
    ROJO = colors.HexColor('#c0392b')
    AMBAR = colors.HexColor('#b9770e')
    VERDE = colors.HexColor('#1e8449')

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    ahora = datetime.now()

    def decorar(canvas, doc):
        canvas.saveState()
        ancho, alto = A4
        canvas.setFillColor(NEGRO)
        canvas.rect(0, alto - 2.6 * cm, ancho, 2.6 * cm, stroke=0, fill=1)
        canvas.setFillColor(ORO)
        canvas.rect(0, alto - 2.75 * cm, ancho, 0.15 * cm, stroke=0, fill=1)
        ruta_logo = os.path.join(settings.BASE_DIR, "inventario", "static", "img", "logo.jpeg")
        x_texto = 1.5 * cm
        if os.path.exists(ruta_logo):
            try:
                canvas.drawImage(ruta_logo, 1.2 * cm, alto - 2.3 * cm, 1.8 * cm, 1.8 * cm,
                                 preserveAspectRatio=True, mask='auto')
                x_texto = 3.4 * cm
            except Exception:
                pass
        canvas.setFillColor(ORO)
        canvas.setFont('Helvetica-Bold', 17)
        canvas.drawString(x_texto, alto - 1.35 * cm, 'REPORTE DE INVENTARIO')
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(x_texto, alto - 1.95 * cm, 'Sistema de Gestión para Barbería')
        canvas.drawRightString(ancho - 1.5 * cm, alto - 1.35 * cm, ahora.strftime('%d/%m/%Y'))
        canvas.drawRightString(ancho - 1.5 * cm, alto - 1.95 * cm, ahora.strftime('%H:%M'))
        canvas.setStrokeColor(BORDE)
        canvas.line(1.5 * cm, 1.4 * cm, ancho - 1.5 * cm, 1.4 * cm)
        canvas.setFillColor(colors.HexColor('#6b5d45'))
        canvas.setFont('Helvetica', 8)
        canvas.drawString(1.5 * cm, 0.9 * cm, 'Generado automáticamente por el sistema')
        canvas.drawRightString(ancho - 1.5 * cm, 0.9 * cm, f'Página {doc.page}')
        canvas.restoreState()

    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=3.4 * cm, bottomMargin=2 * cm,
                            title='Reporte de inventario')
    estilos = getSampleStyleSheet()
    celda = ParagraphStyle('celda', parent=estilos['Normal'], fontSize=9, leading=11)
    titulo = ParagraphStyle('t', parent=estilos['Heading2'], textColor=NEGRO, fontSize=13, spaceAfter=6)
    kpi_txt = ParagraphStyle('k', parent=estilos['Normal'], alignment=TA_CENTER, fontSize=9,
                             textColor=colors.HexColor('#6b5d45'))
    elementos = []

    productos = list(Producto.objects.filter(activo=True).order_by('nombre'))
    total_productos = len(productos)
    stock_total = sum(p.stock_actual for p in productos)
    bajo_stock = sum(1 for p in productos if p.stock_actual <= p.stock_minimo)
    valor_total = sum(p.stock_actual * p.precio_unitario for p in productos)

    kpis = Table([[
        Paragraph(f'<font size=16 color="#1a1410"><b>{total_productos}</b></font><br/>Productos', kpi_txt),
        Paragraph(f'<font size=16 color="#1a1410"><b>{stock_total}</b></font><br/>Unidades en stock', kpi_txt),
        Paragraph(f'<font size=16 color="#c0392b"><b>{bajo_stock}</b></font><br/>Stock bajo / agotado', kpi_txt),
        Paragraph(f'<font size=16 color="#1a1410"><b>$ {valor_total:,.0f}</b></font><br/>Valor del inventario', kpi_txt),
    ]], colWidths=[4.5 * cm] * 4)
    kpis.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CREMA),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDE),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDE),
        ('TOPPADDING', (0, 0), (-1, -1), 8), ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    elementos += [kpis, Paragraph(' ', estilos['Normal']), Paragraph('Detalle de productos', titulo)]

    datos = [['Producto', 'Stock', 'Mín.', 'Máx.', 'Precio', 'Estado']]
    colores_estado = []
    for i, p in enumerate(productos, start=1):
        if p.stock_actual == 0:
            estado, col = 'Agotado', ROJO
        elif p.stock_actual <= p.stock_minimo:
            estado, col = 'Bajo', AMBAR
        else:
            estado, col = 'Disponible', VERDE
        colores_estado.append(('TEXTCOLOR', (5, i), (5, i), col))
        datos.append([Paragraph(p.nombre, celda), str(p.stock_actual), str(p.stock_minimo),
                      str(p.stock_maximo), f'$ {p.precio_unitario:,.0f}', estado])

    tabla = Table(datos, colWidths=[6.2 * cm, 2 * cm, 1.8 * cm, 1.8 * cm, 3 * cm, 3.2 * cm], repeatRows=1)
    tabla.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), NEGRO),
        ('TEXTCOLOR', (0, 0), (-1, 0), ORO),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, CREMA]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, BORDE),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDE),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTNAME', (5, 1), (5, -1), 'Helvetica-Bold'),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ] + colores_estado))
    elementos.append(tabla)

    doc.build(elementos, onFirstPage=decorar, onLaterPages=decorar)
    return response
