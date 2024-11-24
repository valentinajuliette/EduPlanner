from django.contrib import admin
from .models import EventoAcademico, Eventos, Feriados

admin.site.register(EventoAcademico)
admin.site.register(Eventos)
admin.site.register(Feriados)