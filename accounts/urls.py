from django.urls import path

from . import views

urlpatterns = [
    path("perfil/", views.perfil, name="perfil"),
    path("", views.lista_usuarios, name="lista_usuarios"),
    path("nuevo/", views.crear_usuario, name="crear_usuario"),
    path("<int:pk>/editar/", views.editar_usuario, name="editar_usuario"),
    path("<int:pk>/alternar-estado/", views.alternar_estado_usuario, name="alternar_estado_usuario"),
    path("<int:pk>/eliminar/", views.eliminar_usuario, name="eliminar_usuario"),
]
