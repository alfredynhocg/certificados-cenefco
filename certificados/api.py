import hmac
import json
from functools import wraps

from django.conf import settings
from django.db.models import Count, Max
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.utils import timezone
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .generador import limpiar_nombre, normalizar_busqueda
from .models import Estudiante, Lote


def _token_valido(request) -> bool:
    token_configurado = settings.API_TOKEN
    if not token_configurado:
        return False

    encabezado = request.headers.get("Authorization", "")
    if encabezado.startswith("Bearer "):
        token_recibido = encabezado[len("Bearer "):].strip()
    else:
        token_recibido = request.headers.get("X-Api-Key", "").strip()

    if not token_recibido:
        return False
    return hmac.compare_digest(token_recibido, token_configurado)


def requiere_api_token(vista):
    @wraps(vista)
    def envoltura(request, *args, **kwargs):
        if not _token_valido(request):
            return JsonResponse({"error": "No autorizado. Envia un token valido en el header Authorization."}, status=401)
        return vista(request, *args, **kwargs)
    return envoltura


def _lote_a_dict(lote) -> dict:
    total_participantes = getattr(lote, "total_participantes", None)
    if total_participantes is None:
        total_participantes = lote.estudiantes.count()
    return {
        "id": lote.id,
        "curso": lote.curso,
        "estado": lote.estado,
        "estado_display": lote.get_estado_display(),
        "total_participantes": total_participantes,
        "creado_en": lote.creado_en.isoformat(),
    }


@csrf_exempt
@requiere_api_token
@require_http_methods(["GET"])
def api_listar_cursos(request):
    """GET /api/cursos/?q=texto -> lista los lotes (cursos) disponibles para registrar participantes."""
    lotes = list(Lote.objects.annotate(total_participantes=Count("estudiantes")).order_by("-creado_en"))

    q = request.GET.get("q", "").strip()
    if q:
        termino = normalizar_busqueda(q)
        lotes = [lote for lote in lotes if termino in normalizar_busqueda(lote.curso)]

    return JsonResponse({"total": len(lotes), "cursos": [_lote_a_dict(lote) for lote in lotes]})


@csrf_exempt
@requiere_api_token
@require_http_methods(["GET"])
def api_detalle_curso(request, pk):
    """GET /api/cursos/<id>/ -> detalle de un curso (lote) puntual."""
    lote = get_object_or_404(Lote.objects.annotate(total_participantes=Count("estudiantes")), pk=pk)
    return JsonResponse(_lote_a_dict(lote))


@csrf_exempt
@requiere_api_token
@require_http_methods(["POST"])
def api_registrar_estudiantes(request, pk):
    """POST /api/cursos/<id>/estudiantes/ -> registra uno o varios participantes en ese curso.

    Body JSON esperado: {"nombre": "Juan Perez"} o {"nombres": ["Juan Perez", "Maria Gomez"]}
    """
    lote = get_object_or_404(Lote, pk=pk)

    try:
        payload = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "El cuerpo de la peticion debe ser JSON valido."}, status=400)

    if not isinstance(payload, dict):
        return JsonResponse({"error": "El cuerpo de la peticion debe ser un objeto JSON."}, status=400)

    if "nombres" in payload:
        nombres_crudos = payload["nombres"]
        if not isinstance(nombres_crudos, list):
            return JsonResponse({"error": "'nombres' debe ser una lista de texto."}, status=400)
    elif "nombre" in payload:
        nombres_crudos = [payload["nombre"]]
    else:
        return JsonResponse({"error": "Envia 'nombre' (texto) o 'nombres' (lista de texto)."}, status=400)

    nombres_limpios = [limpiar_nombre(n) for n in nombres_crudos]
    nombres_limpios = [n for n in nombres_limpios if n]
    if not nombres_limpios:
        return JsonResponse({"error": "No se recibio ningun nombre valido."}, status=400)

    normalizados_existentes = set(lote.estudiantes.values_list("nombre_normalizado", flat=True))

    duplicados = []
    nombres_a_crear = []
    vistos_en_este_envio = set()
    for nombre in nombres_limpios:
        clave = normalizar_busqueda(nombre)
        if clave in normalizados_existentes or clave in vistos_en_este_envio:
            duplicados.append(nombre)
            continue
        vistos_en_este_envio.add(clave)
        nombres_a_crear.append(nombre)

    if not nombres_a_crear:
        return JsonResponse(
            {
                "error": "El/los participante(s) ya estan registrados en este curso.",
                "duplicados": duplicados,
            },
            status=409,
        )

    hoy = timezone.now().date()
    orden_inicial = (lote.estudiantes.aggregate(maximo=Max("orden"))["maximo"] or 0) + 1
    nuevos = [
        Estudiante(
            lote=lote,
            orden=orden_inicial + indice,
            valor_original=nombre,
            nombre=nombre,
            nombre_normalizado=normalizar_busqueda(nombre),
            fecha_registro=hoy,
        )
        for indice, nombre in enumerate(nombres_a_crear)
    ]
    Estudiante.objects.bulk_create(nuevos)

    return JsonResponse(
        {
            "curso": _lote_a_dict(lote),
            "registrados": [
                {"nombre": estudiante.nombre, "fecha_registro": estudiante.fecha_registro.isoformat()}
                for estudiante in nuevos
            ],
            "duplicados": duplicados,
        },
        status=201,
    )
