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
                messages.error(request, 'Error al registrar.')
                return render(request, 'registro.html', {'form': form})
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
        # Obtener el parámetro de tipo desde la solicitud
        tipo = request.GET.get('tipo', 'todos')

        # Verificar si el usuario está autorizado para ver eventos confidenciales
        tiene_autorizacion = (
            request.user.is_authenticated and 
            (request.user.groups.filter(name='Académicos').exists() or
             request.user.groups.filter(name='Comité Académico').exists())
        )

        # Filtrar eventos académicos
        if tipo == 'todos':
            eventos = EventosAcademicos.objects.all()
        else:
            eventos = EventosAcademicos.objects.filter(tipo=tipo)

        # Excluir eventos confidenciales si el usuario no tiene autorización
        if not tiene_autorizacion:
            eventos = eventos.filter(confidencial=False)

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
            response.raise_for_status()

            # Procesar respuesta
            feriados_data = response.json()
            feriados = [
                {
                    "titulo": feriado.get("nombre"),
                    "descripcion": "Feriado oficial",
                    "fecha_inicio": feriado.get("fecha"),
                    "fecha_fin": feriado.get("fecha"),
                    "tipo": "6",  # Default value for feriados (6. Feriado Nacional)
                    "confidencial": False,
                }
                for feriado in feriados_data
            ]
        except requests.exceptions.RequestException as e:
            feriados = []  # Si hay un error, manejarlo devolviendo una lista vacía

        # Combinar eventos y feriados
        if tipo == 'todos' or tipo == "6":
            calendario = eventos_data + feriados
        else:
            calendario = eventos_data

        # Ordenar cronológicamente
        calendario_ordenado = sorted(calendario, key=lambda x: x['fecha_inicio'])

        return Response(calendario_ordenado, status=status.HTTP_200_OK)

@login_required
def agregar_evento(request):
    # Verificar si el usuario pertenece a los grupos autorizados
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        lista_tipos = dict(EventosAcademicos.LISTA_TIPOS)  # Convertirlo a un diccionario

        # Obtener feriados desde la API de terceros
        url_feriados = "https://apis.digital.gob.cl/fl/feriados/2024"
        headers = {'User-Agent': 'DjangoApp (https://example.com)'}
        try:
            response = requests.get(url_feriados, headers=headers, timeout=10)
            response.raise_for_status()
            feriados = [feriado['fecha'] for feriado in response.json()]
        except requests.exceptions.RequestException as e:
            feriados = []  # Si hay un error, considera que no hay feriados

        if request.method == 'POST':
            titulo = request.POST['titulo']
            descripcion = request.POST.get('descripcion', '')
            fecha_inicio = request.POST['fecha_inicio']
            fecha_fin = request.POST.get('fecha_fin', fecha_inicio)  # Usa fecha_inicio si fecha_fin está vacío
            tipo = request.POST['tipo']
            confidencial = 'confidencial' in request.POST

            # Validación 1: Las fechas no pueden estar en un feriado
            if fecha_inicio in feriados or fecha_fin in feriados:
                messages.error(request, "No se puede agregar un evento en un día feriado.")
                return render(request, 'agregar_evento.html', {'lista_tipos': lista_tipos})

            # Validación 2: La fecha de inicio no puede ser mayor que la fecha de fin
            if fecha_inicio > fecha_fin:
                messages.error(request, "La fecha de inicio no puede ser posterior a la fecha de fin.")
                return render(request, 'agregar_evento.html', {'lista_tipos': lista_tipos})

            # Crear el nuevo evento si pasa las validaciones
            nuevo_evento = EventosAcademicos(
                titulo=titulo,
                descripcion=descripcion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                tipo=tipo,
                confidencial=confidencial,
            )
            nuevo_evento.save()
            messages.success(request, "El evento se agregó exitosamente.")
            return redirect('panel_admin')

        # Renderizar la página del formulario
        return render(request, 'agregar_evento.html', {'lista_tipos': lista_tipos})
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
    # Verificar autorización
    if request.user.groups.filter(name='Académicos').exists() or request.user.groups.filter(name='Comité Académico').exists():
        evento = get_object_or_404(EventosAcademicos, id=evento_id)
        lista_tipos = dict(EventosAcademicos.LISTA_TIPOS)  # Obtener los tipos de evento

        if request.method == 'POST':
            evento.titulo = request.POST.get('titulo')
            evento.descripcion = request.POST.get('descripcion')
            evento.fecha_inicio = request.POST.get('fecha_inicio')
            evento.fecha_fin = request.POST.get('fecha_fin')
            evento.tipo = request.POST.get('tipo')
            evento.confidencial = 'confidencial' in request.POST

            # Validación de fechas
            if evento.fecha_inicio > evento.fecha_fin:
                # Mostrar error si las fechas no son válidas
                messages.error(request, "La fecha de inicio no puede ser posterior a la fecha de fin.")
                return render(request, 'editar_evento.html', {'evento': evento, 'lista_tipos': lista_tipos})
            else:
                evento.save()
                messages.success(request, "El evento se actualizó correctamente.")
            return redirect('panel_admin')

        # Renderizar el formulario con los datos del evento
        return render(request, 'editar_evento.html', {'evento': evento, 'lista_tipos': lista_tipos})
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
