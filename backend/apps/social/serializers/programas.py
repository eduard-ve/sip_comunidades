from rest_framework import serializers
from ..models import EstadoPrograma, ProgramaSocial


class EstadoProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoPrograma
        fields = ['id', 'nombre']


class ProgramaSocialSerializer(serializers.ModelSerializer):
    estado = EstadoProgramaSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoPrograma.objects.all(),
        source='estado',
        write_only=True
    )
    beneficiarios = serializers.PrimaryKeyRelatedField(
        many=True,
        read_only=True  # mostrar IDs de beneficiarios, sin editar
    )
    tipo_programa_display = serializers.CharField(
        source='get_tipo_programa_display',
        read_only=True
    )

    class Meta:
        model = ProgramaSocial
        fields = [
            'id',
            'nombre',
            'descripcion',
            'tipo_programa',
            'tipo_programa_display',
            'estado',
            'estado_id',
            'fecha_inicio',
            'fecha_fin',
            'responsable',
            'beneficiarios',
            'beneficiarios_count'
        ]
