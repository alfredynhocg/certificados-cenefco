from pathlib import Path

import openpyxl
from django.db import migrations


def poblar_estudiantes(apps, schema_editor):
    from certificados.generador import limpiar_nombre

    Lote = apps.get_model("certificados", "Lote")
    Estudiante = apps.get_model("certificados", "Estudiante")

    for lote in Lote.objects.all():
        if not lote.excel:
            continue
        try:
            ruta_excel = Path(lote.excel.path)
            if not ruta_excel.exists():
                continue
            wb = openpyxl.load_workbook(ruta_excel, data_only=True)
            ws = wb.active
        except Exception:
            continue

        estudiantes = []
        orden = 0
        for fila in ws.iter_rows(min_row=1, max_col=2):
            valor_original = fila[0].value
            nombre = limpiar_nombre(valor_original)
            fecha_registro = fila[1].value
            if nombre is None and (valor_original is None or str(valor_original).strip() == ""):
                continue
            orden += 1
            estudiantes.append(Estudiante(
                lote=lote,
                orden=orden,
                valor_original="" if valor_original is None else str(valor_original),
                nombre=nombre or "",
                fecha_registro=fecha_registro if hasattr(fecha_registro, "year") else None,
            ))

        if estudiantes:
            Estudiante.objects.bulk_create(estudiantes)


def eliminar_estudiantes(apps, schema_editor):
    Estudiante = apps.get_model("certificados", "Estudiante")
    Estudiante.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0007_estudiante'),
    ]

    operations = [
        migrations.RunPython(poblar_estudiantes, eliminar_estudiantes),
    ]
