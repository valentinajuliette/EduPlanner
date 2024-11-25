from django.shortcuts import render, redirect, get_object_or_404
from .models import EventosAcademicos
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json
import requests

def calendar_view(request):
    # Obtener eventos académicos desde la base de datos
    eventos = EventosAcademicos.objects.filter(confidencial=False)
    eventos_list = [
        {
            "title": evento.titulo,
            "start": evento.fecha_inicio.strftime('%Y-%m-%d'),
            "end": evento.fecha_fin.strftime('%Y-%m-%d') if evento.fecha_fin else evento.fecha_inicio.strftime('%Y-%m-%d'),
            "description": evento.descripcion,
            "type": "Evento Académico",
        }
        for evento in eventos
    ]

    # Obtener feriados desde la API de terceros
    url_feriados = "https://apis.digital.gob.cl/fl/feriados/2024"
    headers = {'User-Agent': 'DjangoApp (https://example.com)'}
    try:
        response = requests.get(url_feriados, headers=headers, timeout=10)
        response.raise_for_status()
        feriados_data = response.json()
        feriados_list = [
            {
                "title": feriado.get("nombre"),
                "start": feriado.get("fecha"),
                "end": feriado.get("fecha"),
                "description": "Feriado oficial",
                "type": "Feriado",
            }
            for feriado in feriados_data
        ]
    except requests.exceptions.RequestException as e:
        feriados_list = []

    # Combinar ambos tipos de eventos
    calendario = eventos_list + feriados_list

    # Pasar datos al template
    context = {
    "eventos": mark_safe(json.dumps(calendario))
}
    return render(request, 'calendar.html', context)
