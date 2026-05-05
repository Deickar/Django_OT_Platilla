from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from .forms import UserCreateForm, UserEditForm


@staff_member_required
def user_list(request):
    users = User.objects.all().order_by("last_name", "first_name")
    return render(request, "accounts/user_list.html", {"users": users})


@staff_member_required
def user_create(request):
    if request.method == "POST":
        form = UserCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado exitosamente.")
            return redirect("accounts:user_list")
    else:
        form = UserCreateForm()
    return render(request, "accounts/user_form.html", {"form": form, "action": "Crear"})


@staff_member_required
def user_edit(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form = UserEditForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado.")
            return redirect("accounts:user_list")
    else:
        form = UserEditForm(instance=user)
    return render(
        request,
        "accounts/user_form.html",
        {"form": form, "user_obj": user, "action": "Editar"},
    )


@staff_member_required
@require_POST
def user_toggle(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user != request.user:
        user.is_active = not user.is_active
        user.save()
        status = "activado" if user.is_active else "desactivado"
        messages.info(request, f"Usuario {user.username} {status}.")
    return redirect("accounts:user_list")
