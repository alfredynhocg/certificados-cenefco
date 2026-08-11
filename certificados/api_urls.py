from django.urls import path

from . import api

urlpatterns = [
    path("cursos/", api.api_listar_cursos, name="api_listar_cursos"),
    path("cursos/<int:pk>/", api.api_detalle_curso, name="api_detalle_curso"),
    path("cursos/<int:pk>/estudiantes/", api.api_registrar_estudiantes, name="api_registrar_estudiantes"),
]
