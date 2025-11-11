from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count, Q, Avg, F
from datetime import datetime, timedelta
from ..models.personas import Persona
from ..models.relaciones import RelacionFamiliar
from ..serializers.estadisticas import (
    DistribucionEdadSerializer, TopOcupacionSerializer,
    DistribucionEducativaSerializer, LenguaMaternaSerializer,
    DistribucionGeneroSerializer, RelacionFamiliarDetailSerializer
)

class EstadisticasViewSet(viewsets.ViewSet):
    """
    ViewSet para estadísticas de población
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Estadísticas generales para KPIs
        """
        total_personas = Persona.objects.count()

        # Edad promedio
        from django.db.models.functions import ExtractYear
        current_year = datetime.now().year
        edad_promedio = Persona.objects.annotate(
            edad=current_year - ExtractYear('fecha_nacimiento')
        ).aggregate(avg_edad=Avg('edad'))['avg_edad'] or 0

        # Ratio género
        genero_counts = Persona.objects.values('genero').annotate(count=Count('genero'))
        total_m = sum(1 for g in genero_counts if g['genero'] == 'M') and genero_counts.filter(genero='M').first()['count'] or 0
        total_f = sum(1 for g in genero_counts if g['genero'] == 'F') and genero_counts.filter(genero='F').first()['count'] or 0
        ratio_genero = f"{total_m}:{total_f}" if total_f > 0 else f"{total_m}:0"

        # Tasa alfabetismo (personas con nivel educativo > analfabeto)
        alfabetos = Persona.objects.exclude(nivel_educativo__nombre__iexact='analfabeto').count()
        tasa_alfabetismo = (alfabetos / total_personas * 100) if total_personas > 0 else 0

        # Ocupación principal
        ocupacion_principal = Persona.objects.values('ocupacion__nombre').annotate(
            count=Count('ocupacion')
        ).exclude(ocupacion__isnull=True).order_by('-count').first()

        # Lengua materna principal
        lengua_principal = Persona.objects.values('lengua_materna__nombre').annotate(
            count=Count('lengua_materna')
        ).exclude(lengua_materna__isnull=True).order_by('-count').first()

        return Response({
            'poblacion_total': total_personas,
            'edad_promedio': round(edad_promedio, 1),
            'ratio_genero': ratio_genero,
            'tasa_alfabetismo': round(tasa_alfabetismo, 1),
            'ocupacion_principal': ocupacion_principal['ocupacion__nombre'] if ocupacion_principal else None,
            'lengua_materna_principal': lengua_principal['lengua_materna__nombre'] if lengua_principal else None,
        })

    @action(detail=False, methods=['get'])
    def distribucion_edad(self, request):
        """
        Distribución por rangos de edad
        """
        current_year = datetime.now().year
        rangos = [
            (0, 5), (6, 12), (13, 17), (18, 30), (31, 50), (51, 65), (66, 100)
        ]

        data = []
        total_personas = Persona.objects.count()

        for min_edad, max_edad in rangos:
            count = Persona.objects.annotate(
                edad=current_year - ExtractYear('fecha_nacimiento')
            ).filter(edad__gte=min_edad, edad__lte=max_edad).count()

            porcentaje = (count / total_personas * 100) if total_personas > 0 else 0

            data.append({
                'rango_edad': f'{min_edad}-{max_edad}',
                'cantidad': count,
                'porcentaje': round(porcentaje, 1)
            })

        serializer = DistribucionEdadSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def top_ocupaciones(self, request):
        """
        Top 5 ocupaciones
        """
        total_personas = Persona.objects.count()
        ocupaciones = Persona.objects.values('ocupacion__nombre').annotate(
            count=Count('ocupacion')
        ).exclude(ocupacion__isnull=True).order_by('-count')[:5]

        data = []
        for ocupacion in ocupaciones:
            porcentaje = (ocupacion['count'] / total_personas * 100) if total_personas > 0 else 0
            data.append({
                'ocupacion': ocupacion['ocupacion__nombre'],
                'cantidad': ocupacion['count'],
                'porcentaje': round(porcentaje, 1)
            })

        serializer = TopOcupacionSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def distribucion_educativa(self, request):
        """
        Distribución por nivel educativo
        """
        total_personas = Persona.objects.count()
        niveles = Persona.objects.values('nivel_educativo__nombre').annotate(
            count=Count('nivel_educativo')
        ).exclude(nivel_educativo__isnull=True).order_by('nivel_educativo__nombre')

        data = []
        for nivel in niveles:
            porcentaje = (nivel['count'] / total_personas * 100) if total_personas > 0 else 0
            data.append({
                'nivel': nivel['nivel_educativo__nombre'],
                'cantidad': nivel['count'],
                'porcentaje': round(porcentaje, 1)
            })

        serializer = DistribucionEducativaSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def lenguas_maternas(self, request):
        """
        Lenguas maternas con cantidad de hablantes
        """
        total_personas = Persona.objects.count()
        lenguas = Persona.objects.values('lengua_materna__nombre').annotate(
            count=Count('lengua_materna')
        ).exclude(lengua_materna__isnull=True).order_by('-count')

        data = []
        for lengua in lenguas:
            porcentaje = (lengua['count'] / total_personas * 100) if total_personas > 0 else 0
            data.append({
                'lengua': lengua['lengua_materna__nombre'],
                'cantidad': lengua['count'],
                'porcentaje': round(porcentaje, 1)
            })

        serializer = LenguaMaternaSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def distribucion_genero(self, request):
        """
        Distribución por género
        """
        total_personas = Persona.objects.count()
        generos = Persona.objects.values('genero').annotate(count=Count('genero'))

        data = []
        for genero in generos:
            porcentaje = (genero['count'] / total_personas * 100) if total_personas > 0 else 0
            genero_nombre = dict(Persona.GENERO_CHOICES).get(genero['genero'], 'Otro')
            data.append({
                'genero': genero_nombre,
                'cantidad': genero['count'],
                'porcentaje': round(porcentaje, 1)
            })

        serializer = DistribucionGeneroSerializer(data, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def personas_filtradas(self, request):
        """
        Personas filtradas por parámetros
        """
        queryset = Persona.objects.all()

        # Filtros
        edad_min = request.query_params.get('edad_min')
        edad_max = request.query_params.get('edad_max')
        genero = request.query_params.getlist('genero')
        ocupacion_id = request.query_params.get('ocupacion_id')
        nivel_educativo_id = request.query_params.get('nivel_educativo_id')
        estado_civil_id = request.query_params.get('estado_civil_id')
        lengua_id = request.query_params.get('lengua_id')

        current_year = datetime.now().year

        if edad_min:
            min_year = current_year - int(edad_max) if edad_max else current_year - 120
            max_year = current_year - int(edad_min)
            queryset = queryset.filter(fecha_nacimiento__year__gte=min_year, fecha_nacimiento__year__lte=max_year)

        if genero:
            queryset = queryset.filter(genero__in=genero)

        if ocupacion_id:
            queryset = queryset.filter(ocupacion_id=ocupacion_id)

        if nivel_educativo_id:
            queryset = queryset.filter(nivel_educativo_id=nivel_educativo_id)

        if estado_civil_id:
            queryset = queryset.filter(estado_civil_id=estado_civil_id)

        if lengua_id:
            queryset = queryset.filter(lengua_materna_id=lengua_id)

        # Serializar con PersonaSerializer
        from ..serializers.personas import PersonaSerializer
        serializer = PersonaSerializer(queryset, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['get'])
    def relaciones_familiares(self, request, pk=None):
        """
        Relaciones familiares de una persona específica
        """
        try:
            persona = Persona.objects.get(pk=pk)
        except Persona.DoesNotExist:
            return Response({'error': 'Persona no encontrada'}, status=404)

        # Obtener relaciones donde la persona es el origen
        relaciones_origen = RelacionFamiliar.objects.filter(persona=persona).select_related('familiar', 'tipo_relacion')

        # Obtener relaciones donde la persona es el destino (relaciones inversas)
        relaciones_destino = RelacionFamiliar.objects.filter(familiar=persona).select_related('persona', 'tipo_relacion')

        data = []

        # Procesar relaciones de origen
        for relacion in relaciones_origen:
            current_year = datetime.now().year
            edad = current_year - relacion.familiar.fecha_nacimiento.year if relacion.familiar.fecha_nacimiento else None

            data.append({
                'id': relacion.familiar.id,
                'nombre_completo': relacion.familiar.nombre_completo,
                'relacion': relacion.tipo_relacion.nombre,
                'edad': edad,
                'ocupacion': relacion.familiar.ocupacion.nombre if relacion.familiar.ocupacion else None,
            })

        # Procesar relaciones de destino (relaciones inversas)
        for relacion in relaciones_destino:
            current_year = datetime.now().year
            edad = current_year - relacion.persona.fecha_nacimiento.year if relacion.persona.fecha_nacimiento else None

            # Determinar la relación inversa
            relacion_inversa = {
                'Padre': 'Hijo/a',
                'Madre': 'Hijo/a',
                'Hijo': 'Padre/Madre',
                'Hija': 'Padre/Madre',
                'Hermano': 'Hermano/a',
                'Hermana': 'Hermano/a',
                'Pareja': 'Pareja',
                'Esposo': 'Esposa',
                'Esposa': 'Esposo',
            }.get(relacion.tipo_relacion.nombre, relacion.tipo_relacion.nombre)

            data.append({
                'id': relacion.persona.id,
                'nombre_completo': relacion.persona.nombre_completo,
                'relacion': relacion_inversa,
                'edad': edad,
                'ocupacion': relacion.persona.ocupacion.nombre if relacion.persona.ocupacion else None,
            })

        serializer = RelacionFamiliarDetailSerializer(data, many=True)
        return Response(serializer.data)

# Mantener el endpoint anterior por compatibilidad
@api_view(['GET'])
@permission_classes([AllowAny])
def population_stats(request):
    """
    Retorna estadísticas de población para KPIs (legacy)
    """
    # Población total
    total_population = Persona.objects.count()

    # Nacimientos (último año)
    one_year_ago = datetime.now() - timedelta(days=365)
    births = Persona.objects.filter(fecha_nacimiento__gte=one_year_ago).count()

    # Defunciones (simulado - en un sistema real tendrías un modelo de defunciones)
    # Por ahora retornamos un valor simulado
    deaths = 120

    # Crecimiento poblacional (simulado)
    growth_rate = 2.1

    # Estadísticas por género
    gender_stats = Persona.objects.values('genero').annotate(count=Count('genero'))

    # Estadísticas por estado civil
    marital_stats = Persona.objects.values('estado_civil__nombre').annotate(count=Count('estado_civil')).exclude(estado_civil__isnull=True)

    # Estadísticas por nivel educativo
    education_stats = Persona.objects.values('nivel_educativo__nombre').annotate(count=Count('nivel_educativo')).exclude(nivel_educativo__isnull=True)

    return Response({
        'total_population': total_population,
        'births': births,
        'deaths': deaths,
        'growth_rate': growth_rate,
        'gender_distribution': list(gender_stats),
        'marital_status_distribution': list(marital_stats),
        'education_distribution': list(education_stats),
    })