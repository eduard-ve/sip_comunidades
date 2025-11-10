from rest_framework import serializers
from ..models import TipoAutoridad, RolAutoridad, AutoridadComunitaria
from apps.poblacion.serializers.personas import PersonaSerializer


class TipoAutoridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoAutoridad
        fields = ['id', 'nombre', 'descripcion']


class RolAutoridadSerializer(serializers.ModelSerializer):
    class Meta:
        model = RolAutoridad
        fields = ['id', 'nombre', 'descripcion']


class AutoridadComunitariaSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    persona_id = serializers.PrimaryKeyRelatedField(
        queryset=AutoridadComunitaria.objects.all(),
        source='persona',
        write_only=True
    )
    tipo_autoridad = TipoAutoridadSerializer(read_only=True)
    tipo_autoridad_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoAutoridad.objects.all(),
        source='tipo_autoridad',
        write_only=True
    )
    rol = RolAutoridadSerializer(read_only=True)
    rol_id = serializers.PrimaryKeyRelatedField(
        queryset=RolAutoridad.objects.all(),
        source='rol',
        write_only=True
    )

    class Meta:
        model = AutoridadComunitaria
        fields = [
            'id',
            'persona',
            'persona_id',
            'tipo_autoridad',
            'tipo_autoridad_id',
            'rol',
            'rol_id',
            'fecha_inicio_mandato',
            'fecha_fin_mandato',
            'telefono_contacto',
            'email_contacto',
            'observaciones',
            'activo'
        ]