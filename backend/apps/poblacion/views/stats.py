from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.db.models import Count, Q
from datetime import datetime, timedelta
from ..models.personas import Persona

@api_view(['GET'])
@permission_classes([AllowAny])
def population_stats(request):
    """
    Retorna estadísticas de población para KPIs
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