from rest_framework import serializers 
from Calendar.views import EventosAcademicos


# Serializers define the API representation.
class EventoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventosAcademicos
        fields = '__all__'
        #fields = ['nombre','duracion']