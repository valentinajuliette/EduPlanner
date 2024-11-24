from rest_framework import serializers 
from Calendar.views import EventoAcademico


# Serializers define the API representation.
class EventoSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = EventoAcademico
        fields = '__all__'
        #fields = ['nombre','duracion']