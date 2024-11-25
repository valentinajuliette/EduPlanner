from rest_framework import serializers
from Calendar.models import EventosAcademicos

class EventoAcademicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = EventosAcademicos
        fields = '__all__'
