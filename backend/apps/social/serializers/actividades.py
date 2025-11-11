from rest_framework import serializers
from ..models import TipoActividad, EstadoActividad, ActividadComunitaria, AsistenciaActividad
from apps.poblacion.serializers.personas import PersonaSerializer


class TipoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = TipoActividad
        fields = ['id', 'nombre', 'descripcion', 'icono']


class EstadoActividadSerializer(serializers.ModelSerializer):
    class Meta:
        model = EstadoActividad
        fields = ['id', 'nombre', 'descripcion', 'color']


class AsistenciaActividadSerializer(serializers.ModelSerializer):
    persona = PersonaSerializer(read_only=True)
    persona_id = serializers.PrimaryKeyRelatedField(
        queryset=AsistenciaActividad.objects.all(),
        source='persona',
        write_only=True
    )

    class Meta:
        model = AsistenciaActividad
        fields = [
            'id', 'persona', 'persona_id', 'fecha_registro',
            'confirmado', 'fecha_confirmacion', 'observaciones'
        ]


class ActividadComunitariaSerializer(serializers.ModelSerializer):
    tipo_actividad = TipoActividadSerializer(read_only=True)
    tipo_actividad_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoActividad.objects.all(),
        source='tipo_actividad',
        write_only=True
    )
    estado = EstadoActividadSerializer(read_only=True)
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoActividad.objects.all(),
        source='estado',
        write_only=True
    )
    asistentes_registrados = PersonaSerializer(many=True, read_only=True)
    asistencia_detalle = AsistenciaActividadSerializer(source='asistenciaactividad_set', many=True, read_only=True)

    # Campos calculados
    tasa_participacion = serializers.SerializerMethodField()
    asistentes_pendientes = serializers.SerializerMethodField()

    class Meta:
        model = ActividadComunitaria
        fields = [
            'id', 'titulo', 'descripcion', 'tipo_actividad', 'tipo_actividad_id',
            'estado', 'estado_id', 'fecha_inicio', 'fecha_fin', 'ubicacion',
            'capacidad_maxima', 'asistentes_confirmados', 'asistentes_registrados',
            'organizador', 'presupuesto', 'costo_real', 'observaciones',
            'tasa_participacion', 'asistentes_pendientes', 'asistencia_detalle',
            'fecha_creacion', 'fecha_modificacion'
        ]
        read_only_fields = ['fecha_creacion', 'fecha_modificacion']

    def get_tasa_participacion(self, obj):
        return obj.tasa_participacion

    def get_asistentes_pendientes(self, obj):
        return obj.asistentes_pendientes


class ActividadComunitariaCreateSerializer(serializers.ModelSerializer):
    """Serializer específico para creación de actividades"""
    tipo_actividad_id = serializers.PrimaryKeyRelatedField(
        queryset=TipoActividad.objects.all(),
        source='tipo_actividad',
        write_only=True
    )
    estado_id = serializers.PrimaryKeyRelatedField(
        queryset=EstadoActividad.objects.all(),
        source='estado',
        write_only=True
    )

    class Meta:
        model = ActividadComunitaria
        fields = [
            'titulo', 'descripcion', 'tipo_actividad_id', 'estado_id',
            'fecha_inicio', 'fecha_fin', 'ubicacion', 'capacidad_maxima',
            'organizador', 'presupuesto', 'observaciones'
        ]

    def create(self, validated_data):
        # Establecer valores por defecto
        validated_data['asistentes_confirmados'] = 0
        return super().create(validated_data)