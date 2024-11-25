from django.shortcuts import render
from rest_framework import viewsets
from Calendar.models import EventosAcademicos
from .serializers import EventoSerializer

# Create your views here.

class EventosViewSets(viewsets.ModelViewSet):
    serializer_class = EventoSerializer

    def get_queryset(self):
        if self.request.user.groups.filter(name='Académicos').exists() or self.request.user.groups.filter(name='Comité Académico').exists():
            return EventosAcademicos.objects.all()
        else:
            return EventosAcademicos.objects.filter(confidencial=False)