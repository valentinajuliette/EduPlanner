import requests, json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.utils.safestring import mark_safe
from .models import EventoAcademico, Feriados, Eventos
from .serializers import FeriadosSerializer


def pag_principal(request):
    EventoAcademicos = EventoAcademico.objects.all()  # Obtener todos los EventoAcademicos
    return render(request, 'pag_principal.html', {'EventoAcademicos': EventoAcademicos})

def panel_admin(request):
    # Obtener todos los eventos
    eventos = EventoAcademico.objects.all()
    return render(request, 'panel_admin.html', {'eventos': eventos})

def calendar_view(request):
    # Obtener eventos académicos desde la base de datos
    eventos = EventoAcademico.objects.all()
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

def lista_EventoAcademicos(request):
    EventoAcademicos = EventoAcademico.objects.all()
    return render(request, 'lista_EventoAcademicos.html', {'EventoAcademicos': EventoAcademicos})

def agregar_evento(request):
    if request.method == 'POST':
        # Recibir datos del formulario
        titulo = request.POST.get('titulo')
        descripcion = request.POST.get('descripcion')
        fecha_inicio = request.POST.get('fecha_inicio')
        fecha_fin = request.POST.get('fecha_fin')

        # Crear el nuevo evento
        nuevo_evento = EventoAcademico(
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

def editar_evento(request, evento_id):
    # Obtener el evento a editar
    evento = get_object_or_404(EventoAcademico, id=evento_id)
    if request.method == 'POST':
        evento.titulo = request.POST.get('titulo')
        evento.descripcion = request.POST.get('descripcion')
        evento.fecha_inicio = request.POST.get('fecha_inicio')
        evento.fecha_fin = request.POST.get('fecha_fin')
        evento.save()
        return redirect('panel_admin')
    return render(request, 'editar_evento.html', {'evento': evento})

def eliminar_evento(request, evento_id):
    # Obtener el evento y eliminarlo
    evento = get_object_or_404(EventoAcademico, id=evento_id)
    if request.method == 'POST':
        evento.delete()
        return redirect('panel_admin')
    return render(request, 'eliminar_evento.html', {'evento': evento})
class FeriadosAPIView(APIView):
    def get(self, request):
        # Obtener feriados desde la API
        feriados = Feriados.objects.all()
        serializer = FeriadosSerializer(feriados, many=True)
        feriados_data = serializer.data

        # Configuración de la solicitud a la API de feriados
        url_feriados = "https://apis.digital.gob.cl/fl/feriados/2024"
        headers = {
            'User-Agent': 'DjangoApp (https://example.com)'  # Cambia la URL si tienes una
        }
        
        try:
            # Solicitar feriados
            response = requests.get(url_feriados, headers=headers, timeout=10)
            response.raise_for_status()  # Lanza excepción si hay un error HTTP
            
            # Procesar respuesta
            feriados_data = response.json()
            feriados = [
                {
                    "titulo": feriado.get("nombre"),
                    "descripcion": "Feriado oficial",
                    "fecha_inicio": feriado.get("fecha"),
                    "fecha_fin": feriado.get("fecha")
                }
                for feriado in feriados_data
            ]
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error al obtener los feriados: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Combinar y ordenar cronológicamente
        calendario = feriados_data + feriados
        calendario_ordenado = sorted(calendario, key=lambda x: x['fecha_inicio'])

        return Response(calendario_ordenado, status=status.HTTP_200_OK)