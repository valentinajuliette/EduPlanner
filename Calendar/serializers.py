from rest_framework import serializers
from .models import Feriados

class FeriadosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feriados
        fields = '__all__'
