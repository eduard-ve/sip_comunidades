from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from apps.poblacion.models.personas import Persona
from ..models import TipoAutoridad, RolAutoridad, AutoridadComunitaria
from ..serializers.autoridades import (
    TipoAutoridadSerializer,
    RolAutoridadSerializer,
    AutoridadComunitariaSerializer
)


class TipoAutoridadViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar tipos de autoridad comunitaria.
    """
    queryset = TipoAutoridad.objects.all()
    serializer_class = TipoAutoridadSerializer


class RolAutoridadViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar roles de autoridad comunitaria.
    """
    queryset = RolAutoridad.objects.all()
    serializer_class = RolAutoridadSerializer


class AutoridadComunitariaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar autoridades comunitarias.
    """
    queryset = AutoridadComunitaria.objects.select_related(
        'persona', 'tipo_autoridad', 'rol'
    ).all()
    serializer_class = AutoridadComunitariaSerializer

    @action(detail=False, methods=['get'], url_path='buscar-persona')
    def buscar_persona(self, request):
        """
        Busca una persona por número de identificación
        """
        numero_identificacion = request.query_params.get('numero_identificacion', '').strip()

        if not numero_identificacion:
            return Response(
                {'error': 'Número de identificación es requerido'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            persona = get_object_or_404(
                Persona,
                numero_identificacion=numero_identificacion
            )

            # Verificar si ya es autoridad activa
            es_autoridad_activa = AutoridadComunitaria.objects.filter(
                persona=persona,
                activo=True
            ).exists()

            return Response({
                'persona': {
                    'id': persona.id,
                    'numero_identificacion': persona.numero_identificacion,
                    'nombre_completo': persona.nombre_completo,
                    'tipo_identificacion': persona.tipo_identificacion.nombre if persona.tipo_identificacion else None,
                    'fecha_nacimiento': persona.fecha_nacimiento,
                    'genero': persona.genero,
                    'direccion': persona.direccion,
                },
                'es_autoridad_activa': es_autoridad_activa
            })

        except Exception as e:
            return Response(
                {'error': f'Persona no encontrada: {str(e)}'},
                status=status.HTTP_404_NOT_FOUND
            )