from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.template.loader import render_to_string

from .forms import WorkOrderFilterForm, WorkOrderForm
from .models import WorkOrder
from .services import filter_work_orders, generate_orders_pdf, generate_single_order_pdf
from weasyprint import HTML


@login_required
def order_list(request):
    """Vista principal: listado con filtros."""
    form = WorkOrderFilterForm(request.GET or None)
    orders = WorkOrder.objects.select_related("assigned_to", "created_by").all()

    if form.is_valid():
        orders = filter_work_orders(orders, form.cleaned_data)

    context = {
        "orders": orders,
        "filter_form": form,
        "total": orders.count(),
    }
    return render(request, "orders/order_list.html", context)


@login_required
def order_create(request):
    """Crear nueva orden de trabajo."""
    if request.method == "POST":
        form = WorkOrderForm(request.POST)
        if form.is_valid():
            order = form.save(commit=False)
            order.created_by = request.user
            order.save()
            messages.success(request, f"Orden {order.code} creada exitosamente.")
            return redirect("orders:list")
    else:
        form = WorkOrderForm()

    return render(request, "orders/order_form.html", {"form": form, "action": "Crear"})


@login_required
def order_detail(request, pk):
    """Detalle de una orden."""
    order = get_object_or_404(WorkOrder, pk=pk)
    return render(request, "orders/order_detail.html", {"order": order})


@login_required
def order_edit(request, pk):
    """Editar orden existente."""
    order = get_object_or_404(WorkOrder, pk=pk)

    if request.method == "POST":
        form = WorkOrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            messages.success(request, f"Orden {order.code} actualizada.")
            return redirect("orders:detail", pk=pk)
    else:
        form = WorkOrderForm(instance=order)

    return render(
        request,
        "orders/order_form.html",
        {"form": form, "order": order, "action": "Editar"},
    )


@login_required
@require_POST
def order_delete(request, pk):
    """Eliminar orden."""
    order = get_object_or_404(WorkOrder, pk=pk)
    code = order.code
    order.delete()
    messages.warning(request, f"Orden {code} eliminada.")
    return redirect("orders:list")


@login_required
def export_pdf_list(request):
    """Exporta el listado filtrado actual como PDF."""
    form = WorkOrderFilterForm(request.GET or None)
    orders = WorkOrder.objects.select_related("assigned_to", "created_by").all()

    if form.is_valid():
        orders = filter_work_orders(orders, form.cleaned_data)

    buffer = generate_orders_pdf(orders)
    response = HttpResponse(buffer, content_type="application/pdf")
    response["Content-Disposition"] = 'attachment; filename="ordenes_trabajo.pdf"'
    return response


@login_required
def export_pdf_weasy(request, pk):
    """Exporta el detalle de una orden como PDF usando WeasyPrint."""
    order = get_object_or_404(WorkOrder, pk=pk)
    html_string = render_to_string("orders/pdf_orden.html", {"orden": order})
    pdf = HTML(string=html_string).write_pdf()
    response = HttpResponse(pdf, content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="{order.code}.pdf"'
    return response
