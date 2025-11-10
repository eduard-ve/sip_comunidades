from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from django.shortcuts import get_object_or_404
from django.db import transaction
from .models import Encuesta, Pregunta, Opcion, Respuesta
from .serializers import (
    EncuestaSerializer, PreguntaSerializer, OpcionSerializer,
    RespuestaSerializer, EncuestaCreateSerializer
)

# ViewSets para los modelos de encuestas
class EncuestaViewSet(viewsets.ModelViewSet):
    queryset = Encuesta.objects.all()
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        if self.action == 'create':
            return EncuestaCreateSerializer
        return EncuestaSerializer

    def get_queryset(self):
        """Filtrar encuestas por usuario si es necesario"""
        return Encuesta.objects.all().order_by('-fecha_creacion')

    def create(self, request, *args, **kwargs):
        """Crear encuesta con manejo de transacciones"""
        try:
            with transaction.atomic():
                return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({
                'error': 'Datos de entrada inválidos',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({
                'error': 'Error interno del servidor',
                'details': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(detail=False, methods=['get'], permission_classes=[permissions.AllowAny])
    def by_token(self, request):
        """Obtener encuesta por token para respuestas públicas"""
        token = request.query_params.get('token')
        if not token:
            return Response({
                'error': 'Token requerido',
                'message': 'Se requiere un token válido para acceder a la encuesta'
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Convertir token a entero para buscar por ID
            encuesta_id = int(token)
            encuesta = Encuesta.objects.get(id_encuesta=encuesta_id, estado='activa')

            # Usar el serializador estándar que ya incluye las preguntas
            serializer = self.get_serializer(encuesta)
            data = serializer.data

            return Response(data)
        except (Encuesta.DoesNotExist, ValueError):
            return Response({
                'error': 'Encuesta no encontrada',
                'message': 'La encuesta no existe o no está disponible'
            }, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({
                'error': 'Error interno',
                'message': str(e)
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class PreguntaViewSet(viewsets.ModelViewSet):
    queryset = Pregunta.objects.all()
    serializer_class = PreguntaSerializer
    permission_classes = [permissions.IsAuthenticated]

class OpcionViewSet(viewsets.ModelViewSet):
    queryset = Opcion.objects.all()
    serializer_class = OpcionSerializer
    permission_classes = [permissions.IsAuthenticated]

class RespuestaViewSet(viewsets.ModelViewSet):
    queryset = Respuesta.objects.all()
    serializer_class = RespuestaSerializer
    permission_classes = [permissions.AllowAny]  # Permitir respuestas públicas

    def get_queryset(self):
        """Filtrar respuestas por encuesta si se especifica"""
        queryset = Respuesta.objects.all()
        encuesta_id = self.request.query_params.get('encuesta', None)
        if encuesta_id:
            queryset = queryset.filter(encuesta_id=encuesta_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Crear respuesta con validaciones adicionales"""
        try:
            # Validar que la encuesta existe y está activa
            encuesta_id = request.data.get('encuesta')
            if encuesta_id:
                try:
                    encuesta = Encuesta.objects.get(id_encuesta=encuesta_id, estado='activa')
                except Encuesta.DoesNotExist:
                    return Response({
                        'error': 'Encuesta no válida',
                        'message': 'La encuesta no existe o no está disponible'
                    }, status=status.HTTP_400_BAD_REQUEST)

            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({
                'error': 'Datos de respuesta inválidos',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        """Filtrar respuestas por encuesta si se especifica"""
        queryset = Respuesta.objects.all()
        encuesta_id = self.request.query_params.get('encuesta', None)
        if encuesta_id:
            queryset = queryset.filter(encuesta_id=encuesta_id)
        return queryset

    def create(self, request, *args, **kwargs):
        """Crear respuesta con validaciones adicionales"""
        try:
            # Validar que la encuesta existe y está activa
            encuesta_id = request.data.get('encuesta')
            if encuesta_id:
                try:
                    encuesta = Encuesta.objects.get(id=encuesta_id, estado='activa')
                except Encuesta.DoesNotExist:
                    return Response({
                        'error': 'Encuesta no válida',
                        'message': 'La encuesta no existe o no está disponible'
                    }, status=status.HTTP_400_BAD_REQUEST)

            return super().create(request, *args, **kwargs)
        except ValidationError as e:
            return Response({
                'error': 'Datos de respuesta inválidos',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)
