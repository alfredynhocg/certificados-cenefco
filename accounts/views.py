from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CambiarPasswordForm, PerfilForm, UsuarioChangeForm, UsuarioCreationForm
from .models import Usuario


def es_admin(user):
    return user.is_authenticated and user.es_admin


@login_required
def perfil(request):
    form_perfil = PerfilForm(instance=request.user)
    form_password = CambiarPasswordForm(request.user)

    if request.method == "POST":
        accion = request.POST.get("accion")
        if accion == "perfil":
            form_perfil = PerfilForm(request.POST, instance=request.user)
            if form_perfil.is_valid():
                form_perfil.save()
                messages.success(request, "Tu perfil se actualizo correctamente.")
                return redirect("perfil")
        elif accion == "password":
            form_password = CambiarPasswordForm(request.user, request.POST)
            if form_password.is_valid():
                usuario = form_password.save()
                update_session_auth_hash(request, usuario)
                messages.success(request, "Tu contrasena se actualizo correctamente.")
                return redirect("perfil")

    return render(request, "accounts/perfil.html", {
        "form_perfil": form_perfil,
        "form_password": form_password,
    })


@login_required
@user_passes_test(es_admin)
def lista_usuarios(request):
    usuarios = Usuario.objects.all().order_by("username")
    return render(request, "accounts/lista_usuarios.html", {"usuarios": usuarios})


@login_required
@user_passes_test(es_admin)
def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario creado correctamente.")
            return redirect("lista_usuarios")
    else:
        form = UsuarioCreationForm()
    return render(request, "accounts/crear_usuario.html", {"form": form})


@login_required
@user_passes_test(es_admin)
def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == "POST":
        form = UsuarioChangeForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, "Usuario actualizado correctamente.")
            return redirect("lista_usuarios")
    else:
        form = UsuarioChangeForm(instance=usuario)
    return render(request, "accounts/editar_usuario.html", {"form": form, "usuario": usuario})


@login_required
@user_passes_test(es_admin)
def alternar_estado_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if usuario.pk == request.user.pk:
        messages.error(request, "No puedes desactivar tu propia cuenta.")
        return redirect("lista_usuarios")

    if request.method == "POST":
        usuario.is_active = not usuario.is_active
        usuario.save(update_fields=["is_active"])
        if usuario.is_active:
            messages.success(request, f'Usuario "{usuario.username}" habilitado. Ya puede iniciar sesion.')
        else:
            messages.success(request, f'Usuario "{usuario.username}" deshabilitado. Ya no podra iniciar sesion, pero su cuenta y sus lotes se conservan.')

    return redirect("lista_usuarios")


@login_required
@user_passes_test(es_admin)
def eliminar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if usuario.pk == request.user.pk:
        messages.error(request, "No puedes eliminar tu propia cuenta.")
        return redirect("lista_usuarios")

    if request.method == "POST":
        nombre = usuario.username
        usuario.delete()
        messages.success(request, f'Usuario "{nombre}" eliminado.')
        return redirect("lista_usuarios")

    total_lotes = usuario.lotes.count()
    return render(request, "accounts/eliminar_usuario.html", {"usuario": usuario, "total_lotes": total_lotes})
