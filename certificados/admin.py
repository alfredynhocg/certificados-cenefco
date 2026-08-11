from django.contrib import admin

from .models import Estudiante, Lote

@admin.register(Lote)
class LoteAdmin(admin.ModelAdmin):
    list_display = ("curso", "propietario", "estado", "total_certificados", "creado_en")
    list_filter = ("estado", "propietario")
    search_fields = ("curso", "propietario__username")


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("nombre", "lote", "orden", "fecha_registro")
    list_filter = ("lote",)
    search_fields = ("nombre", "valor_original", "lote__curso")
