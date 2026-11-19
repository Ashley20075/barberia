"""Identidad visual común de los PDFs (negro / dorado / crema, igual que la página)."""
import os
from datetime import datetime

from django.conf import settings
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, TableStyle

ORO = colors.HexColor('#d4a017')
NEGRO = colors.HexColor('#1a1410')
CREMA = colors.HexColor('#faf5ea')
BORDE = colors.HexColor('#e3d7bd')
TEXTO_SUAVE = colors.HexColor('#6b5d45')
ROJO = colors.HexColor('#c0392b')
VERDE = colors.HexColor('#1e8449')
AMBAR = colors.HexColor('#b9770e')

ANCHO_UTIL = 18 * cm  # A4 con márgenes de 1.5 cm


def _estilos():
    base = getSampleStyleSheet()
    return {
        'celda': ParagraphStyle('celda', parent=base['Normal'], fontSize=9, leading=11),
        'seccion': ParagraphStyle('seccion', parent=base['Heading2'], textColor=NEGRO,
                                  fontSize=13, spaceBefore=10, spaceAfter=6),
        'kpi': ParagraphStyle('kpi', parent=base['Normal'], alignment=TA_CENTER, fontSize=9,
                              textColor=TEXTO_SUAVE, leading=13),
        'normal': base['Normal'],
    }


ESTILOS = _estilos()


def ruta_logo():
    ruta = os.path.join(settings.BASE_DIR, 'inventario', 'static', 'img', 'logo.jpeg')
    return ruta if os.path.exists(ruta) else None


def pagina_con_encabezado(titulo, subtitulo=''):
    """Devuelve el callback para onFirstPage/onLaterPages con banda negra, filete dorado y pie."""
    ahora = datetime.now()

    def decorar(canvas, doc):
        canvas.saveState()
        ancho, alto = A4
        canvas.setFillColor(NEGRO)
        canvas.rect(0, alto - 2.6 * cm, ancho, 2.6 * cm, stroke=0, fill=1)
        canvas.setFillColor(ORO)
        canvas.rect(0, alto - 2.75 * cm, ancho, 0.15 * cm, stroke=0, fill=1)
        x_texto = 1.5 * cm
        logo = ruta_logo()
        if logo:
            try:
                canvas.drawImage(logo, 1.2 * cm, alto - 2.3 * cm, 1.8 * cm, 1.8 * cm,
                                 preserveAspectRatio=True, mask='auto')
                x_texto = 3.4 * cm
            except Exception:
                pass
        canvas.setFillColor(ORO)
        canvas.setFont('Helvetica-Bold', 17)
        canvas.drawString(x_texto, alto - 1.35 * cm, titulo.upper())
        canvas.setFillColor(colors.white)
        canvas.setFont('Helvetica', 9)
        canvas.drawString(x_texto, alto - 1.95 * cm, subtitulo or 'Barber Springfield · Sistema de Gestión')
        canvas.drawRightString(ancho - 1.5 * cm, alto - 1.35 * cm, ahora.strftime('%d/%m/%Y'))
        canvas.drawRightString(ancho - 1.5 * cm, alto - 1.95 * cm, ahora.strftime('%H:%M'))
        canvas.setStrokeColor(BORDE)
        canvas.line(1.5 * cm, 1.4 * cm, ancho - 1.5 * cm, 1.4 * cm)
        canvas.setFillColor(TEXTO_SUAVE)
        canvas.setFont('Helvetica', 8)
        canvas.drawString(1.5 * cm, 0.9 * cm, 'Barber Springfield · Generado automáticamente')
        canvas.drawRightString(ancho - 1.5 * cm, 0.9 * cm, f'Página {doc.page}')
        canvas.restoreState()

    return decorar


def crear_documento(response, titulo, subtitulo=''):
    doc = SimpleDocTemplate(response, pagesize=A4, leftMargin=1.5 * cm, rightMargin=1.5 * cm,
                            topMargin=3.4 * cm, bottomMargin=2 * cm, title=titulo)
    return doc, pagina_con_encabezado(titulo, subtitulo)


def tarjetas_resumen(items):
    """items: lista de (valor, etiqueta, color_hex_opcional)."""
    celdas = []
    for it in items:
        valor, etiqueta = it[0], it[1]
        color = it[2] if len(it) > 2 else '#1a1410'
        celdas.append(Paragraph(f'<font size=15 color="{color}"><b>{valor}</b></font><br/>{etiqueta}',
                                ESTILOS['kpi']))
    t = Table([celdas], colWidths=[ANCHO_UTIL / len(celdas)] * len(celdas))
    t.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), CREMA),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDE),
        ('INNERGRID', (0, 0), (-1, -1), 0.5, BORDE),
        ('TOPPADDING', (0, 0), (-1, -1), 9), ('BOTTOMPADDING', (0, 0), (-1, -1), 9),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
    ]))
    return t


def titulo_seccion(texto):
    return Paragraph(texto, ESTILOS['seccion'])


def tabla(datos, anchos_cm, centradas=(), cabecera=NEGRO, texto_cabecera=ORO, extra=()):
    """Tabla con cabecera de marca, filas alternadas y celdas con ajuste de línea."""
    filas = []
    for i, fila in enumerate(datos):
        if i == 0:
            filas.append([str(c) for c in fila])
        else:
            filas.append([c if not isinstance(c, str) else Paragraph(c, ESTILOS['celda']) for c in fila])
    t = Table(filas, colWidths=[a * cm for a in anchos_cm], repeatRows=1)
    estilo = [
        ('BACKGROUND', (0, 0), (-1, 0), cabecera),
        ('TEXTCOLOR', (0, 0), (-1, 0), texto_cabecera),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 9),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, CREMA]),
        ('LINEBELOW', (0, 0), (-1, -1), 0.4, BORDE),
        ('BOX', (0, 0), (-1, -1), 0.8, BORDE),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6), ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]
    for c in centradas:
        estilo.append(('ALIGN', (c, 0), (c, -1), 'CENTER'))
    t.setStyle(TableStyle(estilo + list(extra)))
    return t
