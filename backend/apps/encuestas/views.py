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
        """Crear respuestas en bulk con validaciones adicionales"""
        try:
            # Verificar si es una lista de respuestas (bulk create)
            if isinstance(request.data, list):
                return self.bulk_create(request)
            else:
                # Crear respuesta individual
                return self.create_single(request)
        except ValidationError as e:
            return Response({
                'error': 'Datos de respuesta inválidos',
                'details': e.detail
            }, status=status.HTTP_400_BAD_REQUEST)

    def create_single(self, request):
        """Crear una respuesta individual"""
        # Validar que la encuesta existe y está activa
        encuesta_id = request.data.get('encuesta')
        if encuesta_id:
            try:
                Encuesta.objects.get(id_encuesta=encuesta_id, estado='activa')
            except Encuesta.DoesNotExist:
                return Response({
                    'error': 'Encuesta no válida',
                    'message': 'La encuesta no existe o no está disponible'
                }, status=status.HTTP_400_BAD_REQUEST)

        return super().create(request)

    def bulk_create(self, request):
        """Crear múltiples respuestas en una sola transacción"""
        respuestas_data = request.data

        if not respuestas_data:
            return Response({
                'error': 'Datos requeridos',
                'message': 'Se requieren datos de respuestas'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Validar que todas las respuestas pertenezcan a la misma encuesta activa
        encuesta_ids = set()
        for respuesta_data in respuestas_data:
            encuesta_id = respuesta_data.get('encuesta')
            if not encuesta_id:
                return Response({
                    'error': 'Encuesta requerida',
                    'message': 'Cada respuesta debe incluir el ID de la encuesta'
                }, status=status.HTTP_400_BAD_REQUEST)
            encuesta_ids.add(encuesta_id)

        if len(encuesta_ids) != 1:
            return Response({
                'error': 'Encuesta única requerida',
                'message': 'Todas las respuestas deben pertenecer a la misma encuesta'
            }, status=status.HTTP_400_BAD_REQUEST)

        encuesta_id = list(encuesta_ids)[0]
        try:
            Encuesta.objects.get(id_encuesta=encuesta_id, estado='activa')
        except Encuesta.DoesNotExist:
            return Response({
                'error': 'Encuesta no válida',
                'message': 'La encuesta no existe o no está disponible'
            }, status=status.HTTP_400_BAD_REQUEST)

        # Crear respuestas en bulk
        respuestas_creadas = []
        with transaction.atomic():
            for respuesta_data in respuestas_data:
                serializer = self.get_serializer(data=respuesta_data)
                serializer.is_valid(raise_exception=True)
                respuesta = serializer.save()
                respuestas_creadas.append(respuesta)

        # Serializar las respuestas creadas
        result_serializer = self.get_serializer(respuestas_creadas, many=True)
        return Response(result_serializer.data, status=status.HTTP_201_CREATED)
