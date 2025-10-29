from rest_framework import serializers
from ..models import EstadoPrograma, ProgramaSocial

# Serializer para el modelo EstadoPrograma y ProgramaSocial
class EstadoProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPrograma
        fields = ['id', 'nombre']

class ProgramaSocialSerializer(serializers.ModelSerializer):
    estado = EstadoProgramaSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoPrograma.objects.all(), source='estado', writwe_only=True
    )

    class Meta:
        model = ProgramaSocial
        fields = ['id', 'nombre', 'descripcion', 'estado', 'estado_id', 'fecha_inicio', 'fecha_fin', 'responsable']