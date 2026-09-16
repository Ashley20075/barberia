from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import models
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
            producto = form.save()
            messages.success(request, f'✅ Producto "{producto.nombre}" agregado exitosamente.')
            return redirect('inventario:dashboard')
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

            # Límites de stock (máx. 20 / mín. 5 en ajustes)
            if datos['tipo'] == 'ENTRADA' and producto.stock_actual + datos['cantidad'] > 20:
                messages.error(request, "❌ No se puede superar el stock máximo de 20 unidades.")
                return redirect('inventario:dashboard')

            if datos['tipo'] == 'AJUSTE' and datos['cantidad'] > 20:
                messages.error(request, "❌ El stock máximo permitido es de 20 unidades.")
                return redirect('inventario:dashboard')

            if datos['tipo'] == 'AJUSTE' and datos['cantidad'] < 5:
                messages.error(request, "❌ El stock mínimo permitido es de 5 unidades.")
                return redirect('inventario:dashboard')

            try:
                movimiento = registrar_movimiento(
                    producto=producto,
                    tipo=datos['tipo'],
                    cantidad=datos['cantidad'],
                    usuario=request.user,
                    proveedor=datos.get('proveedor'),
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
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="reporte_inventario.pdf"'

    doc = SimpleDocTemplate(response)

    estilos = getSampleStyleSheet()
    elementos = []

    # ================= LOGO =================

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

    # ================= TITULO =================

    elementos.append(
        Paragraph(
            "<b>REPORTE DE INVENTARIO</b>",
            estilos['Title']
        )
    )

    elementos.append(
        Paragraph(
            "Sistema de Gestión para Barbería",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"Fecha de generación: {datetime.now().strftime('%d/%m/%Y %H:%M')}",
            estilos['Normal']
        )
    )

    elementos.append(Paragraph(" ", estilos['Normal']))

    # ================= TABLA =================

    datos = [[
        "Producto",
        "Stock",
        "Stock mínimo",
        "Precio",
        "Estado"
    ]]

    productos = Producto.objects.filter(
        activo=True
    ).order_by("nombre")

    for producto in productos:

        if producto.stock_actual == 0:
            estado = "Agotado"

        elif producto.stock_actual <= producto.stock_minimo:
            estado = "Bajo"

        else:
            estado = "Disponible"

        datos.append([
            producto.nombre,
            str(producto.stock_actual),
            str(producto.stock_minimo),
            f"$ {producto.precio_unitario}",
            estado
        ])

    tabla = Table(datos)

    tabla.setStyle(TableStyle([

        ('BACKGROUND', (0,0), (-1,0), colors.black),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),

        ('GRID', (0,0), (-1,-1), 1, colors.black),

        ('BACKGROUND', (0,1), (-1,-1), colors.beige),

        ('ALIGN', (0,0), (-1,-1), 'CENTER'),

        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),

        ('BOTTOMPADDING', (0,0), (-1,0), 10),

    ]))

    elementos.append(tabla)

    elementos.append(Paragraph(" ", estilos['Normal']))

    # ================= RESUMEN =================

    total_productos = Producto.objects.filter(
        activo=True
    ).count()

    stock_total = Producto.objects.filter(
        activo=True
    ).aggregate(
        total=Sum('stock_actual')
    )['total'] or 0

    bajo_stock = Producto.objects.filter(
        activo=True,
        stock_actual__lte=models.F('stock_minimo')
    ).count()

    elementos.append(
        Paragraph(
            f"<b>Total de productos:</b> {total_productos}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Stock total:</b> {stock_total}",
            estilos['Normal']
        )
    )

    elementos.append(
        Paragraph(
            f"<b>Productos con bajo stock:</b> {bajo_stock}",
            estilos['Normal']
        )
    )

    doc.build(elementos)

    return response