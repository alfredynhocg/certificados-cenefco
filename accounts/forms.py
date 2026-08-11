from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, UserCreationForm

from .models import Usuario

INPUT_CLASES = (
    "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm shadow-sm "
    "focus:border-brand-500 focus:ring-2 focus:ring-brand-100 focus:outline-none"
)


def _aplicar_estilos(form):
    for field in form.fields.values():
        clases_previas = field.widget.attrs.get("class", "")
        field.widget.attrs["class"] = f"{clases_previas} {INPUT_CLASES}".strip()


class LoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_estilos(self)


class UsuarioCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        _aplicar_estilos(self)


class UsuarioChangeForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("username", "first_name", "last_name", "email", "rol", "is_active")
        widgets = {
            "is_active": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300 text-brand-600 cursor-pointer"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["is_active"].label = "Usuario activo (puede iniciar sesion)"
        for nombre, field in self.fields.items():
            if nombre == "is_active":
                continue
            clases_previas = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{clases_previas} {INPUT_CLASES}".strip()


class PerfilForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ("first_name", "last_name", "email")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["first_name"].label = "Nombres"
        self.fields["last_name"].label = "Apellidos"
        _aplicar_estilos(self)


class CambiarPasswordForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["old_password"].label = "Contrasena actual"
        self.fields["new_password1"].label = "Contrasena nueva"
        self.fields["new_password2"].label = "Confirmar contrasena nueva"
        _aplicar_estilos(self)
