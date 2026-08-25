
import json
import re
import random
import requests
from datetime import datetime

from django.http import JsonResponse
from django.views.decorators.http import require_POST, require_GET
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from model.models import Cliente, Boleto, TipoBoleto

# URL MySQL 
WEB_SERVICE_URL = 'http://127.0.0.1:8001/web_service'


def index(request):
    return render(request, 'comprar_boleto.html')


# ─────────────────────────────────────────────────────────────
#  Vista GET: carteleras desde web service MySQL
# ─────────────────────────────────────────────────────────────
@require_GET
def listar_carteleras(request):
    try:
        response = requests.get(f'{WEB_SERVICE_URL}/cartelera/')
        response.raise_for_status()
        carteleras = response.json()

        data = [
            {
                'value': c['id_cartelera'],
                'label': c['nombre'] or c['id_cartelera'],
            }
            for c in carteleras
        ]
        return JsonResponse({'ok': True, 'carteleras': data})

    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {'ok': False, 'error': 'No se pudo conectar al web service.'},
            status=503
        )
    except Exception as e:
        return JsonResponse(
            {'ok': False, 'error': f'Error al obtener carteleras: {str(e)}'},
            status=500
        )


# ─────────────────────────────────────────────────────────────
#  Vista GET: películas por cartelera desde web service MySQL
# ─────────────────────────────────────────────────────────────
@require_GET
def listar_peliculas(request):
    id_cartelera = request.GET.get('cartelera', '').strip()

    if not id_cartelera:
        return JsonResponse(
            {'ok': False, 'error': 'Parámetro "cartelera" es requerido.'},
            status=400
        )

    try:
        response = requests.get(f'{WEB_SERVICE_URL}/pelicula/')
        response.raise_for_status()
        todas = response.json()

        # Filtrar por cartelera del lado Python
        peliculas = [
            p for p in todas
            if str(p.get('id_cartelera')) == str(id_cartelera)
        ]

        data = [
            {
                'value': str(p['id_pelicula']),
                'label': p['titulo'],
                'clasificacion': p.get('clasificacion') or 'N/A',
                'duracion': p.get('duracion'),
            }
            for p in peliculas
        ]

        return JsonResponse({'ok': True, 'peliculas': data})

    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {'ok': False, 'error': 'No se pudo conectar al web service.'},
            status=503
        )
    except Exception as e:
        return JsonResponse(
            {'ok': False, 'error': f'Error al obtener películas: {str(e)}'},
            status=500
        )


# ─────────────────────────────────────────────────────────────
#  Vista POST: genera y guarda el boleto
# ─────────────────────────────────────────────────────────────
@csrf_exempt
@require_POST
def generar_boleto(request):

    # ── 1. Parsear JSON ─────────────────────────────────────
    try:
        body = json.loads(request.body)
    except json.JSONDecodeError:
        return JsonResponse(
            {'ok': False, 'error': 'Cuerpo de la petición inválido.'},
            status=400
        )

    # ── 2. Extraer campos ───────────────────────────────────
    cedula       = body.get('cedula',      '').strip()
    nombres      = body.get('nombres',     '').strip()
    apellidos    = body.get('apellidos',   '').strip()
    telefono     = body.get('telefono',    '').strip()
    correo       = body.get('correo',      '').strip()
    direccion    = body.get('direccion',   '').strip()
    id_cartelera = body.get('cartelera',   '').strip()
    id_pelicula  = body.get('pelicula',    '').strip()
    tipo_boleto  = body.get('tipo_boleto', '').strip()

    # ── 3. Validar campos obligatorios ──────────────────────
    campos = {
        'cédula':         cedula,
        'nombres':        nombres,
        'apellidos':      apellidos,
        'teléfono':       telefono,
        'correo':         correo,
        'dirección':      direccion,
        'cartelera':      id_cartelera,
        'película':       id_pelicula,
        'tipo de boleto': tipo_boleto,
    }
    for nombre_campo, valor in campos.items():
        if not valor:
            return JsonResponse(
                {'ok': False, 'error': f'El campo "{nombre_campo}" es obligatorio.'},
                status=400
            )

    # ── 4. Validar cédula: exactamente 10 caracteres ────────
    if len(cedula) != 10:
        return JsonResponse(
            {'ok': False, 'error': 'La cédula debe tener exactamente 10 caracteres.'},
            status=400
        )

    # ── 5. Validar teléfono: exactamente 10 dígitos ─────────
    if not re.fullmatch(r'\d{10}', telefono):
        return JsonResponse(
            {'ok': False, 'error': 'El teléfono debe tener exactamente 10 dígitos numéricos.'},
            status=400
        )

    # ── 6. Validar correo ────────────────────────────────────
    if '@' not in correo or '.com' not in correo:
        return JsonResponse(
            {'ok': False, 'error': 'El correo debe contener "@" y la extensión ".com".'},
            status=400
        )

    # ── 7. Validar tipo de boleto ────────────────────────────
    if tipo_boleto not in ['VIP', 'GENERAL','NIÑOS']:
        return JsonResponse(
            {'ok': False, 'error': 'Tipo de boleto no válido. Use "VIP","NIÑOS" o "GENERAL"'},
            status=400
        )

    # ── 8. Validar cartelera existe en web service ───────────
    try:
        response = requests.get(f'{WEB_SERVICE_URL}/cartelera/')
        response.raise_for_status()
        carteleras = response.json()
        cartelera_obj = next(
            (c for c in carteleras if str(c['id_cartelera']) == str(id_cartelera)),
        )
        if not cartelera_obj:
            return JsonResponse(
                {'ok': False, 'error': f'La cartelera "{id_cartelera}" no existe.'},
                status=400
            )
    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {'ok': False, 'error': 'No se pudo conectar al web service.'},
            status=503
        )

    # ── 9. Validar película pertenece a la cartelera ─────────
    try:
        response = requests.get(f'{WEB_SERVICE_URL}/pelicula/')
        response.raise_for_status()
        peliculas = response.json()
        pelicula_obj = next(
            (p for p in peliculas
            if str(p['id_pelicula']) == str(id_pelicula)
            and str(p['id_cartelera']) == str(id_cartelera)),
            None
        )
        if not pelicula_obj:
            return JsonResponse(
                {'ok': False, 'error': 'La película no pertenece a la cartelera seleccionada.'},
                status=400
            )
    except requests.exceptions.ConnectionError:
        return JsonResponse(
            {'ok': False, 'error': 'No se pudo conectar al web service.'},
            status=503
        )

    # ── 10. Obtener TipoBoleto desde PostgreSQL ──────────────
    try:
        tipo_obj = TipoBoleto.objects.using('default').get(nombre=tipo_boleto)
    except TipoBoleto.DoesNotExist:
        return JsonResponse(
            {'ok': False, 'error': f'Tipo de boleto "{tipo_boleto}" no encontrado en BD.'},
            status=400
        )

    # ── 11. Guardar / actualizar Cliente en PostgreSQL ───────
    cliente, _ = Cliente.objects.using('default').update_or_create(
        cedula_cliente=cedula,
        defaults={
            'nombres':         nombres,
            'apellidos':       apellidos,
            'numero_telefono': telefono,
            'correo':          correo,
            'direccion':       direccion,
        }
    )

    # ── 12. Generar datos automáticos ────────────────────────
    sala    = random.randint(1, 10)
    asiento = random.randint(1, 40)
    cajero  = f'CAJ{random.randint(1, 10):03d}'
    ahora   = datetime.now()
    precio = 10.00 if tipo_boleto == 'VIP' else 5.00 if tipo_boleto == 'GENERAL' else 3.50

    # ── 13. Guardar Boleto en PostgreSQL ─────────────────────
    boleto = Boleto.objects.using('default').create(
        id_cajero      = cajero,
        cedula_cliente = cliente,
        id_tipo_boleto = tipo_obj,
        numero_sala    = sala,
        id_pelicula    = str(id_pelicula),
        asiento        = asiento,
        hora           = ahora.time(),
        fecha          = ahora.date(),
        precio         = precio,
    )

    # ── 14. Retornar ticket ──────────────────────────────────
    return JsonResponse({
        'ok': True,
        'ticket': {
            'numero_boleto': boleto.numero_boleto,
            'cliente':       f'{nombres} {apellidos} ({cedula})',
            'cartelera':     cartelera_obj['nombre'] or id_cartelera,
            'pelicula':      pelicula_obj['titulo'],
            'sala':          sala,
            'asiento':       asiento,
            'cajero':        cajero,
            'fecha':         ahora.strftime('%d/%m/%Y'),
            'hora':          ahora.strftime('%H:%M'),
            'tipo_boleto':   tipo_boleto,
            'precio':        f'${precio:.2f}',
        }
    }, status=201)