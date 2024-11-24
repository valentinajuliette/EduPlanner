from django.shortcuts import redirect, render
from django.http import JsonResponse
from django.utils.safestring import mark_safe
import json
import requests
from .models import EventosAcademicos

def calendar_view(request):
    # Obtener eventos académicos desde la base de datos
    eventos = EventosAcademicos.objects.all()
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

def agregar_evento(request):
    if request.method == 'POST':
        # Recibir datos del formulario
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Crear el nuevo evento
        nuevo_evento = EventosAcademicos(
            titulo=titulo,
            descripcion=descripcion,
            fecha_inicio=fecha_inicio,
            fecha_fin=fecha_fin
        )
        nuevo_evento.save()

        # Redirigir al calendario o página principal
        return redirect('calendar_view')  # Cambiar a la ruta que desees

    # Renderizar la página del formulario
    return render(request, 'agregar_evento.html')