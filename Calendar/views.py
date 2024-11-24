from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import EventosAcademicos

# Create your views here.
def calendar_view(request):
    eventos = EventosAcademicos.objects.all()
    
    data = {
        "eventos": eventos
    }
    return render(request,'calendar.html',data)