from django.shortcuts import render
from rest_framework import viewsets
from Calendar.models import EventoAcademico
from .serializers import EventoSerializer

# Create your views here.

class EventosViewSets(viewsets.ModelViewSet):
    queryset = EventoAcademico.objects.all()
    #Aca podemos Filtrar y Procesar del queryset
    serializer_class = EventoSerializer
