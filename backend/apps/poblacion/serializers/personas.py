from rest_framework import serializers
from apps.poblacion.models.personas import Persona

class PersonaSerializer(serializers.ModelSerializer):
    tipo_indentificacion_nombre = serializers.CharField(source='tipo_identificacion.nombre', read_only=True)
    nivel_educativo_nombre = serializers.CharField(source='nivel_educativo.nombre', read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'