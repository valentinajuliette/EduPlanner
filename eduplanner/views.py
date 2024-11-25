import requests
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import EventoAcademicoSerializer
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from Calendar.views import EventosAcademicos
from .forms import RegistroForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def pag_principal(request):
    EventoAcademicos = EventosAcademicos.objects.all()  # Obtener todos los EventoAcademicos
    return render(request, 'pag_principal.html', {'EventoAcademicos': EventoAcademicos})

def registro(request):
    if request.user.is_authenticated:
    # Do something for authenticated users.
        return redirect('pag_principal')
    else:
            # Do something for anonymous users.
        if request.method == 'POST':
            form = RegistroForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, 'Registro exitoso. Ahora puedes iniciar sesión.')
                return redirect('login')
        else:
            form = RegistroForm()
        return render(request, 'registro.html', {'form': form})

def iniciar_sesion(request):
    if request.user.is_authenticated:
        # Do something for authenticated users.
        return redirect('pag_principal')
    else:
        # Do something for anonymous users.
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('pag_principal')  # Redirige a la página principal después del login.
            else:
                messages.error(request, 'Usuario o contraseña incorrectos.')
        return render(request, 'login.html')

def cerrar_sesion(request):
    logout(request)
    return redirect('login')

class CalendarioAPIView(APIView): 
    def get(self, request):
        # Obtener eventos académicos desde la base de datos
        eventos = EventosAcademicos.objects.all()
        serializer = EventoAcademicoSerializer(eventos, many=True)
        eventos_data = serializer.data

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
                    "fecha_fin": feriado.get("fecha"),
                    "tipo": 6 # Default value for feriados (6. Feriado Nacional)
                }
                for feriado in feriados_data
            ]
        except requests.exceptions.RequestException as e:
            return Response(
                {"error": f"Error al obtener los feriados: {str(e)}"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        # Combinar y ordenar cronológicamente
        calendario = eventos_data + feriados
        calendario_ordenado = sorted(calendario, key=lambda x: x['fecha_inicio'])

        return Response(calendario_ordenado, status=status.HTTP_200_OK)

@login_required
def agregar_evento(request):
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        if request.method == 'POST':
            # Recibir datos del formulario
            titulo = request.POST.get('titulo')
            descripcion = request.POST.get('descripcion')
            fecha_inicio = request.POST.get('fecha_inicio')
            fecha_fin = request.POST.get('fecha_fin')
            tipo = 6 #tipo = request.POST.get('tipo')
            
            # Crear el nuevo evento
            nuevo_evento = EventosAcademicos(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo=tipo
            )
            nuevo_evento.save()

            # Redirigir al panel
            return redirect('panel_admin')

        # Renderizar la página del formulario
        return render(request, 'agregar_evento.html')
    else:
        return redirect('pag_principal')

@login_required
def panel_admin(request):
    # Obtener todos los eventos
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        eventos = EventosAcademicos.objects.all()
        return render(request, 'panel_admin.html', {'eventos': eventos})
    else:
        return redirect('pag_principal')

@login_required
def editar_evento(request, evento_id):
    # Obtener el evento a editar
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        evento = get_object_or_404(EventosAcademicos, id=evento_id)
        if request.method == 'POST':
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.tipo = request.POST.get('tipo')
            evento.save()
            return redirect('panel_admin')
        return render(request, 'editar_evento.html', {'evento': evento})
    else:
        return redirect('pag_principal')

@login_required
def eliminar_evento(request, evento_id):
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        # Obtener el evento y eliminarlo
        evento = get_object_or_404(EventosAcademicos, id=evento_id)
        if request.method == 'POST':
            evento.delete()
            return redirect('panel_admin')
        return render(request, 'eliminar_evento.html', {'evento': evento})
    else:
        return redirect('pag_principal')
