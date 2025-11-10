from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.utils import timezone
from apps.poblacion.models.personas import Persona
from ..models import TipoActividad, EstadoActividad, ActividadComunitaria, AsistenciaActividad
from ..serializers.actividades import (
    TipoActividadSerializer,
    EstadoActividadSerializer,
    ActividadComunitariaSerializer,
    ActividadComunitariaCreateSerializer,
    AsistenciaActividadSerializer
)


class TipoActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar tipos de actividad comunitaria.
    """
    queryset = TipoActividad.objects.all()
    serializer_class = TipoActividadSerializer


class EstadoActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar estados de actividad.
    """
    queryset = EstadoActividad.objects.all()
    serializer_class = EstadoActividadSerializer


class ActividadComunitariaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar actividades comunitarias.
    """
    queryset = ActividadComunitaria.objects.select_related(
        'tipo_actividad', 'estado'
    ).prefetch_related('asistentes_registrados').all()
    serializer_class = ActividadComunitariaSerializer

    def get_serializer_class(self):
        if self.action == 'create':
            return ActividadComunitariaCreateSerializer
        return ActividadComunitariaSerializer

    @action(detail=True, methods=['post'], url_path='registrar-asistencia')
    def registrar_asistencia(self, request, pk=None):
        """
        Registra la asistencia de una persona a una actividad
        """
        actividad = self.get_object()
        persona_id = request.data.get('persona_id')
        confirmado = request.data.get('confirmado', False)
        observaciones = request.data.get('observaciones', '')

        if not persona_id:
            return Response(
                {'error': 'ID de persona es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            persona = get_object_or_404(Persona, id=persona_id)

            # Verificar si ya está registrado
            asistencia, created = AsistenciaActividad.objects.get_or_create(
                actividad=actividad,
                persona=persona,
                defaults={
                    'confirmado': confirmado,
                    'observaciones': observaciones
                }
            )

            if not created:
                # Actualizar registro existente
                asistencia.confirmado = confirmado
                asistencia.observaciones = observaciones
                if confirmado and not asistencia.fecha_confirmacion:
                    asistencia.fecha_confirmacion = timezone.now()
                asistencia.save()

            # Actualizar contadores en la actividad
            actividad.asistentes_confirmados = actividad.asistenciaactividad_set.filter(confirmado=True).count()
            actividad.save()

            serializer = AsistenciaActividadSerializer(asistencia)
            return Response(serializer.data, status=status.HTTP_200_OK if not created else status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                {'error': f'Error al registrar asistencia: {str(e)}'},
                status=status.HTTP_400_BAD_REQUEST
            )

    @action(detail=True, methods=['get'], url_path='estadisticas')
    def estadisticas(self, request, pk=None):
        """
        Obtiene estadísticas de participación de la actividad
        """
        actividad = self.get_object()

        total_registrados = actividad.asistentes_registrados.count()
        total_confirmados = actividad.asistentes_confirmados
        tasa_participacion = actividad.tasa_participacion

        stats = {
            'total_registrados': total_registrados,
            'total_confirmados': total_confirmados,
            'tasa_participacion': round(tasa_participacion, 2),
            'capacidad_maxima': actividad.capacidad_maxima,
            'disponibilidad': actividad.capacidad_maxima - total_registrados if actividad.capacidad_maxima else None
        }

        return Response(stats)

    @action(detail=False, methods=['get'], url_path='calendario')
    def calendario(self, request):
        """
        Obtiene actividades para mostrar en calendario
        """
        fecha_inicio = request.query_params.get('fecha_inicio')
        fecha_fin = request.query_params.get('fecha_fin')

        queryset = self.get_queryset()

        if fecha_inicio:
            queryset = queryset.filter(fecha_inicio__date__gte=fecha_inicio)
        if fecha_fin:
            queryset = queryset.filter(fecha_inicio__date__lte=fecha_fin)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)


class AsistenciaActividadViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite gestionar asistencias a actividades.
    """
    queryset = AsistenciaActividad.objects.select_related('actividad', 'persona').all()
    serializer_class = AsistenciaActividadSerializer

    @action(detail=False, methods=['get'], url_path='por-actividad')
    def por_actividad(self, request):
        """
        Obtiene asistencias filtradas por actividad
        """
        actividad_id = request.query_params.get('actividad_id')
        if not actividad_id:
            return Response(
                {'error': 'ID de actividad es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        asistencias = self.get_queryset().filter(actividad_id=actividad_id)
        serializer = self.get_serializer(asistencias, many=True)
        return Response(serializer.data)