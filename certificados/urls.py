from django.urls import path

from . import views

urlpatterns = [
    path("dashboard/", views.dashboard, name="dashboard"),
    path("estadisticas/", views.estadisticas, name="estadisticas"),
    path("estadisticas/exportar/excel/", views.exportar_estadisticas_excel, name="exportar_estadisticas_excel"),
    path("estadisticas/exportar/pdf/", views.exportar_estadisticas_pdf, name="exportar_estadisticas_pdf"),
    path("lotes/nuevo/", views.crear_lote, name="crear_lote"),
    path("lotes/<int:pk>/", views.detalle_lote, name="detalle_lote"),
    path("lotes/<int:pk>/editar/", views.editar_lote, name="editar_lote"),
    path("lotes/<int:pk>/eliminar/", views.eliminar_lote, name="eliminar_lote"),
    path("lotes/<int:pk>/duplicar/", views.duplicar_lote, name="duplicar_lote"),
    path("lotes/<int:pk>/previsualizar/", views.previsualizar_lote, name="previsualizar_lote"),
    path("lotes/<int:pk>/estudiantes/", views.lista_estudiantes, name="lista_estudiantes"),
    path("lotes/<int:pk>/estudiantes/agregar/", views.agregar_estudiantes, name="agregar_estudiantes"),
    path("lotes/<int:pk>/estudiantes/capitalizacion/", views.cambiar_capitalizacion, name="cambiar_capitalizacion"),
    path("lotes/<int:pk>/estudiantes/<int:fila>/editar/", views.editar_estudiante, name="editar_estudiante"),
    path("lotes/<int:pk>/estudiantes/<int:fila>/eliminar/", views.eliminar_estudiante, name="eliminar_estudiante"),
    path("lotes/<int:pk>/estudiantes/<int:fila>/descargar/", views.descargar_certificado_individual, name="descargar_certificado_individual"),
    path("lotes/<int:pk>/estudiantes/<int:fila>/generar/", views.generar_certificado_individual, name="generar_certificado_individual"),
    path("lotes/<int:pk>/estudiantes/descargar/", views.descargar_certificados, name="descargar_certificados"),
    path("lotes/<int:pk>/estudiantes/exportar/", views.exportar_reporte, name="exportar_reporte"),
    path("lotes/<int:pk>/exportar/", views.exportar_paquete_curso, name="exportar_paquete_curso"),
    path("lotes/<int:pk>/generar/", views.generar_lote, name="generar_lote"),
    path("lotes/<int:pk>/progreso/", views.progreso_lote, name="progreso_lote"),
    path("lotes/<int:pk>/descargar/", views.descargar_zip, name="descargar_zip"),
]
