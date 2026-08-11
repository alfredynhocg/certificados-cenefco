from django import forms

from .models import Lote

INPUT_CLASES = (
    "block w-full rounded-lg border border-slate-300 px-3 py-2 text-sm shadow-sm "
    "focus:border-brand-500 focus:ring-2 focus:ring-brand-100 focus:outline-none"
)

CLASES_ARCHIVO = (
    "block w-full text-sm text-slate-500 rounded-lg border border-slate-300 shadow-sm "
    "file:mr-3 file:py-2 file:px-3 file:rounded-md file:border-0 file:bg-brand-50 "
    "file:text-brand-700 file:text-sm file:font-medium hover:file:bg-brand-100 "
    "focus:border-brand-500 focus:ring-2 focus:ring-brand-100 focus:outline-none"
)

FUENTES_DISPONIBLES = [
    ("Helvetica", "Helvetica"),
    ("Helvetica-Bold", "Helvetica Negrita"),
    ("Helvetica-Oblique", "Helvetica Italica"),
    ("Times-Roman", "Times Roman"),
    ("Times-Bold", "Times Negrita"),
    ("Times-Italic", "Times Italica"),
    ("Courier", "Courier"),
    ("Courier-Bold", "Courier Negrita"),
]


class LoteForm(forms.ModelForm):
    fuente = forms.ChoiceField(choices=FUENTES_DISPONIBLES, label="Fuente")

    class Meta:
        model = Lote
        fields = [
            "curso",
            "excel",
            "plantilla",
            "texto_x",
            "texto_y",
            "margen_izquierdo",
            "margen_derecho",
            "tamano_fuente",
            "tamano_fuente_min",
            "color_texto",
            "fuente",
            "qr_activo",
            "qr_contenido",
            "qr_x",
            "qr_y",
            "qr_tamano",
        ]
        widgets = {
            "texto_x": forms.HiddenInput(),
            "texto_y": forms.HiddenInput(),
            "color_texto": forms.TextInput(attrs={"type": "color", "class": "h-10 w-16 rounded-md border border-slate-300 cursor-pointer p-1"}),
            "qr_x": forms.HiddenInput(),
            "qr_y": forms.HiddenInput(),
            "qr_activo": forms.CheckboxInput(attrs={"class": "h-5 w-5 rounded border-slate-300 text-brand-600 cursor-pointer"}),
            "qr_contenido": forms.TextInput(attrs={"placeholder": "https://tusitio.com/validar?codigo={codigo}"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields["excel"].required = False
            self.fields["plantilla"].required = False
        self.fields["qr_contenido"].required = False
        for nombre, field in self.fields.items():
            if nombre in ("texto_x", "texto_y", "color_texto", "qr_x", "qr_y", "qr_activo"):
                continue
            clases_previas = field.widget.attrs.get("class", "")
            clases_base = CLASES_ARCHIVO if nombre in ("excel", "plantilla") else INPUT_CLASES
            field.widget.attrs["class"] = f"{clases_previas} {clases_base}".strip()

    def clean(self):
        datos = super().clean()
        if datos.get("qr_activo") and not datos.get("qr_contenido"):
            self.add_error("qr_contenido", "Escribe el texto o la URL que codificara el QR.")
        return datos
