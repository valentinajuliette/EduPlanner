from django.shortcuts import render
from rest_framework import viewsets
from Calendar.models import EventosAcademicos
from .serializers import EventoSerializer

# Create your views here.

class EventosViewSets(viewsets.ModelViewSet):
    queryset = EventosAcademicos.objects.filter(confidencial=False)
    serializer_class = EventoSerializer

        