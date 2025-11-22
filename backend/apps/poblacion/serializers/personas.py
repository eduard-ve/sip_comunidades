from rest_framework import serializers
from ..models.personas import Persona

class PersonaSerializer(serializers.ModelSerializer):
    tipo_identificacion_nombre = serializers.CharField(source='tipo_identificacion.nombre', read_only=True)
    nivel_educativo_nombre = serializers.CharField(source='nivel_educativo.nombre', read_only=True)
    ocupacion_nombre = serializers.CharField(source='ocupacion.nombre', read_only=True)
    grupo_etnico_nombre = serializers.CharField(source='grupo_etnico.nombre', read_only=True)
    estado_civil_nombre = serializers.CharField(source='estado_civil.nombre', read_only=True)
    lengua_materna_nombre = serializers.CharField(source='lengua_materna.nombre', read_only=True)
    nombre_completo = serializers.CharField(read_only=True)

    class Meta:
        model = Persona
        fields = '__all__'