"""
Servicios de negocio — lógica desacoplada de las vistas.
"""
from io import BytesIO
from django.db.models import QuerySet
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from .models import WorkOrder


# ── Filtrado ──────────────────────────────────────────────────────────────────

def filter_work_orders(queryset: QuerySet, filters: dict) -> QuerySet:
    """Aplica filtros al queryset de órdenes."""
    if filters.get('status'):
        queryset = queryset.filter(status=filters['status'])
    if filters.get('priority'):
        queryset = queryset.filter(priority=filters['priority'])
    if filters.get('assigned_to'):
        queryset = queryset.filter(assigned_to=filters['assigned_to'])
    if filters.get('search'):
        term = filters['search']
        queryset = queryset.filter(title__icontains=term) | queryset.filter(code__icontains=term)
    return queryset


# ── Generación de PDF ─────────────────────────────────────────────────────────

def generate_orders_pdf(orders: QuerySet) -> BytesIO:
    """Genera un PDF con el listado de órdenes filtradas."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                             leftMargin=0.75 * inch, rightMargin=0.75 * inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('CustomTitle', parent=styles['Title'],
                                  fontSize=16, textColor=colors.HexColor('#0d6efd'))
    sub_style = ParagraphStyle('Sub', parent=styles['Normal'],
                                fontSize=9, textColor=colors.grey)

    story = [
        Paragraph("Reporte de Órdenes de Trabajo", title_style),
        Paragraph(f"Total de registros: {orders.count()}", sub_style),
        Spacer(1, 0.25 * inch),
    ]

    # Encabezados de tabla
    headers = ['Código', 'Título', 'Estado', 'Prioridad', 'Asignado a', 'Fecha límite']
    data = [headers]

    for order in orders:
        data.append([
            order.code,
            order.title[:45] + ('…' if len(order.title) > 45 else ''),
            order.get_status_display(),
            order.get_priority_display(),
            order.assigned_to.get_full_name() or order.assigned_to.username if order.assigned_to else '—',
            order.due_date.strftime('%d/%m/%Y') if order.due_date else '—',
        ])

    table = Table(data, colWidths=[0.9*inch, 2.4*inch, 1.0*inch, 0.9*inch, 1.3*inch, 1.0*inch])
    table.setStyle(TableStyle([
        ('BACKGROUND',   (0, 0), (-1, 0),  colors.HexColor('#0d6efd')),
        ('TEXTCOLOR',    (0, 0), (-1, 0),  colors.white),
        ('FONTNAME',     (0, 0), (-1, 0),  'Helvetica-Bold'),
        ('FONTSIZE',     (0, 0), (-1, 0),  9),
        ('ALIGN',        (0, 0), (-1, -1), 'CENTER'),
        ('VALIGN',       (0, 0), (-1, -1), 'MIDDLE'),
        ('FONTSIZE',     (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#f8f9fa')]),
        ('GRID',         (0, 0), (-1, -1), 0.5, colors.HexColor('#dee2e6')),
        ('TOPPADDING',   (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING',(0, 0), (-1, -1), 6),
    ]))

    story.append(table)
    doc.build(story)
    buffer.seek(0)
    return buffer


def generate_single_order_pdf(order: WorkOrder) -> BytesIO:
    """Genera un PDF detallado para una orden individual."""
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter,
                             leftMargin=inch, rightMargin=inch,
                             topMargin=0.75 * inch, bottomMargin=0.75 * inch)

    styles = getSampleStyleSheet()
    title_style = ParagraphStyle('T', parent=styles['Title'], fontSize=18,
                                  textColor=colors.HexColor('#0d6efd'))
    label_style = ParagraphStyle('L', parent=styles['Normal'], fontSize=9,
                                  textColor=colors.grey, spaceBefore=6)
    value_style = ParagraphStyle('V', parent=styles['Normal'], fontSize=11)

    story = [
        Paragraph(f"Orden de Trabajo: {order.code}", title_style),
        Spacer(1, 0.2 * inch),
    ]

    fields = [
        ('Título',      order.title),
        ('Estado',      order.get_status_display()),
        ('Prioridad',   order.get_priority_display()),
        ('Asignado a',  order.assigned_to.get_full_name() if order.assigned_to else '—'),
        ('Creado por',  order.created_by.get_full_name() or order.created_by.username),
        ('Fecha límite', order.due_date.strftime('%d/%m/%Y') if order.due_date else '—'),
        ('Creado el',   order.created_at.strftime('%d/%m/%Y %H:%M')),
    ]

    for label, value in fields:
        story.append(Paragraph(label, label_style))
        story.append(Paragraph(str(value), value_style))

    story.append(Spacer(1, 0.2 * inch))
    story.append(Paragraph('Descripción', label_style))
    story.append(Paragraph(order.description, value_style))

    doc.build(story)
    buffer.seek(0)
    return buffer
