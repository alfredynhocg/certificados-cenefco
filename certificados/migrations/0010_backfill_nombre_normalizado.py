from django.db import migrations


def backfill_nombre_normalizado(apps, schema_editor):
    from certificados.generador import normalizar_busqueda

    Estudiante = apps.get_model("certificados", "Estudiante")
    for estudiante in Estudiante.objects.filter(nombre_normalizado="").iterator():
        estudiante.nombre_normalizado = normalizar_busqueda(estudiante.nombre or estudiante.valor_original)
        estudiante.save(update_fields=["nombre_normalizado"])


def limpiar_nombre_normalizado(apps, schema_editor):
    Estudiante = apps.get_model("certificados", "Estudiante")
    Estudiante.objects.update(nombre_normalizado="")


class Migration(migrations.Migration):

    dependencies = [
        ('certificados', '0009_estudiante_nombre_normalizado'),
    ]

    operations = [
        migrations.RunPython(backfill_nombre_normalizado, limpiar_nombre_normalizado),
    ]
