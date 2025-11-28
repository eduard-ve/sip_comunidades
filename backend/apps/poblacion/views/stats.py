from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import viewsets
from django.db.models import Count, Q, Avg, F
from django.db.models.functions import ExtractYear
from datetime import datetime, timedelta
from ..models.personas import Persona
from ..models.relaciones import RelacionFamiliar
from ..serializers.estadisticas import (
    DistribucionEdadSerializer, TopOcupacionSerializer,
    DistribucionEducativaSerializer, LenguaMaternaSerializer,
    DistribucionGeneroSerializer, RelacionFamiliarDetailSerializer
)
from apps.social.models import ProgramaSocial, AutoridadComunitaria, ActividadComunitaria
from apps.salud.models import RegistroSalud, AlertaSalud, ControlSalud

class EstadisticasViewSet(viewsets.ViewSet):
    """
    ViewSet para estadísticas de población
    """
    permission_classes = [AllowAny]

    @action(detail=False, methods=['get'])
    def estadisticas(self, request):
        """
        Estadísticas generales para KPIs principales
        """
        total_personas = Persona.objects.count()

        # Edad promedio
        current_year = datetime.now().year
        edad_promedio = Persona.objects.annotate(
            edad=current_year - ExtractYear('fecha_nacimiento')
        ).aggregate(avg_edad=Avg('edad'))['avg_edad'] or 0

        # Tasa alfabetismo (personas con nivel educativo > analfabeto)
        alfabetos = Persona.objects.exclude(nivel_educativo__nombre__iexact='analfabeto').count()
        tasa_alfabetismo = (alfabetos / total_personas * 100) if total_personas > 0 else 0

        # Ocupación principal
        ocupacion_principal = Persona.objects.values('ocupacion__nombre').annotate(
            count=Count('ocupacion')
        ).exclude(ocupacion__isnull=True).order_by('-count').first()

        # Crecimiento poblacional (simulado basado en nacimientos recientes)
        # En un sistema real, esto vendría de datos históricos
        crecimiento_poblacional = 2.1  # porcentaje anual simulado

        return Response({
            'poblacion_total': total_personas,
            'edad_promedio': round(edad_promedio, 1),
            'tasa_alfabetismo': round(tasa_alfabetismo, 1),
            'ocupacion_principal': ocupacion_principal['ocupacion__nombre'] if ocupacion_principal else None,
            'crecimiento_poblacional': crecimiento_poblacional,
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
    def dashboard(self, request):
        """
        Estadísticas agregadas para el dashboard ejecutivo
        """
        # Datos de población
        total_personas = Persona.objects.count()

        # Promedio familiar (simulado basado en relaciones)
        # En un sistema real, esto vendría de datos de hogares/familias
        promedio_familiar = 3.6  # valor simulado

        # Tasa de alfabetización
        alfabetos = Persona.objects.exclude(nivel_educativo__nombre__iexact='analfabeto').count()
        tasa_alfabetismo = (alfabetos / total_personas * 100) if total_personas > 0 else 0

        # Tasa de empleo (personas con ocupación, excluyendo desempleados)
        ocupados = Persona.objects.exclude(ocupacion__isnull=True).exclude(ocupacion__nombre='Desempleado').count()
        # Población económicamente activa = ocupados + desempleados
        pea = ocupados + Persona.objects.filter(ocupacion__nombre='Desempleado').count()
        tasa_empleo = (ocupados / pea * 100) if pea > 0 else 0

        # Datos sociales
        programas_activos = ProgramaSocial.objects.filter(estado__nombre__iexact='activo').count()
        beneficiarios_totales = ProgramaSocial.objects.aggregate(
            total=Count('beneficiarios_count')
        )['total'] or 0
        autoridades_activas = AutoridadComunitaria.objects.filter(activo=True).count()
        actividades_realizadas = ActividadComunitaria.objects.filter(
            estado__nombre__iexact='completada'
        ).count()

        # Próximas actividades (próximos 30 días)
        from django.utils import timezone
        proximas_actividades = ActividadComunitaria.objects.filter(
            fecha_inicio__gte=timezone.now(),
            fecha_inicio__lte=timezone.now() + timedelta(days=30)
        ).order_by('fecha_inicio')[:2]

        proximas_actividades_data = []
        for act in proximas_actividades:
            proximas_actividades_data.append({
                'nombre': act.titulo,  # Cambiado de 'nombre' a 'titulo'
                'tipo': act.tipo_actividad.nombre if act.tipo_actividad else 'Sin tipo',
                'fecha': act.fecha_inicio.strftime('%d/%m/%Y') if act.fecha_inicio else None
            })

        # Autoridades activas
        autoridades = AutoridadComunitaria.objects.filter(activo=True).select_related('persona', 'rol')[:2]
        autoridades_data = []
        for auth in autoridades:
            autoridades_data.append({
                'rol': auth.rol.nombre if auth.rol else 'Sin rol',
                'nombre': auth.persona.nombre_completo if auth.persona else 'Sin nombre'
            })

        # Datos de salud
        registros_salud = RegistroSalud.objects.count()
        alertas_activas = AlertaSalud.objects.filter(resuelta=False).count()
        controles_pendientes = ControlSalud.objects.filter(realizado=False).count()

        # Distribución por género
        genero_data = Persona.objects.values('genero').annotate(count=Count('genero'))
        genero_dict = {}
        for g in genero_data:
            genero_nombre = dict(Persona.GENERO_CHOICES).get(g['genero'], 'Otro')
            genero_dict[genero_nombre.lower()] = g['count']

        total_genero = sum(genero_dict.values())
        genero_porcentajes = {}
        for key, value in genero_dict.items():
            genero_porcentajes[key] = round((value / total_genero * 100), 1) if total_genero > 0 else 0

        # Distribución por edad
        current_year = datetime.now().year
        edad_ranges = [
            (0, 5), (6, 12), (13, 17), (18, 30), (31, 50), (51, 65), (66, 120)
        ]

        edad_hombres = []
        edad_mujeres = []

        for min_age, max_age in edad_ranges:
            # Hombres
            count_h = Persona.objects.filter(genero='M').annotate(
                edad=current_year - ExtractYear('fecha_nacimiento')
            ).filter(edad__gte=min_age, edad__lte=max_age).count()
            edad_hombres.append(count_h)

            # Mujeres
            count_m = Persona.objects.filter(genero='F').annotate(
                edad=current_year - ExtractYear('fecha_nacimiento')
            ).filter(edad__gte=min_age, edad__lte=max_age).count()
            edad_mujeres.append(count_m)

        # Ocupación por género (excluyendo desempleados)
        ocupacion_hombres = Persona.objects.filter(
            genero='M', ocupacion__isnull=False
        ).exclude(ocupacion__nombre='Desempleado').count()
        ocupacion_mujeres = Persona.objects.filter(
            genero='F', ocupacion__isnull=False
        ).exclude(ocupacion__nombre='Desempleado').count()

        # Desocupación por género (personas con ocupación "Desempleado")
        desocupacion_hombres = Persona.objects.filter(
            genero='M', ocupacion__nombre='Desempleado'
        ).count()
        desocupacion_mujeres = Persona.objects.filter(
            genero='F', ocupacion__nombre='Desempleado'
        ).count()

        total_hombres = Persona.objects.filter(genero='M').count()
        total_mujeres = Persona.objects.filter(genero='F').count()

        ocupacion_hombres_pct = (ocupacion_hombres / total_hombres * 100) if total_hombres > 0 else 0
        ocupacion_mujeres_pct = (ocupacion_mujeres / total_mujeres * 100) if total_mujeres > 0 else 0
        desocupacion_hombres_pct = (desocupacion_hombres / total_hombres * 100) if total_hombres > 0 else 0
        desocupacion_mujeres_pct = (desocupacion_mujeres / total_mujeres * 100) if total_mujeres > 0 else 0

        # Programas por tipo (simulado - no hay campo tipo_programa en el modelo)
        programas_radar = [4, 5, 3, 2, 5]  # Valores simulados para Salud, Educación, Cultural, Infraestructura, Asistencia

        return Response({
            'hero_metrics': {
                'poblacion': {
                    'value': f'{total_personas:,}',
                    'label': 'Población Total',
                    'sublabel': f'{int(total_personas / promedio_familiar):,} familias',
                    'trend': 2.8,
                    'color': '#3b82f6'
                },
                'familiar': {
                    'value': f'{promedio_familiar}',
                    'label': 'Promedio Familiar',
                    'sublabel': 'Personas/hogar',
                    'trend': 0.5,
                    'color': '#10b981'
                },
                'educacion': {
                    'value': f'{tasa_alfabetismo:.0f}%',
                    'label': 'Cobertura Educativa',
                    'sublabel': 'Alfabetización',
                    'trend': 3.2,
                    'color': '#f59e0b'
                },
                'empleo': {
                    'value': f'{tasa_empleo:.0f}%',
                    'label': 'Tasa de Empleo',
                    'sublabel': 'Población activa',
                    'trend': -1.2,
                    'color': '#ef4444'
                }
            },
            'indicadores_compactos': {
                'dependencia': {'value': '61.4%', 'label': 'Tasa de Dependencia', 'color': '#ff7043'},
                'servicios': {'value': '88%', 'label': 'Hogares con Servicios', 'color': '#42a5f5'},
                'alfabetizacion': {'value': f'{tasa_alfabetismo:.1f}%', 'label': 'Alfabetización', 'color': '#10b981'},
                'familiar': {'value': f'{int(total_personas / promedio_familiar):,}', 'label': 'Total Familias', 'color': '#f59e0b'}
            },
            'gestion_social': [
                {'label': 'Programas Activos', 'value': programas_activos, 'color': '#17a2b8'},
                {'label': 'Beneficiarios Totales', 'value': beneficiarios_totales, 'color': '#fd7e14'},
                {'label': 'Autoridades Activas', 'value': autoridades_activas, 'color': '#28a745'},
                {'label': 'Actividades Realizadas', 'value': actividades_realizadas, 'color': '#6f42c1'}
            ],
            'programas_tipo_radar': {
                'labels': ['Salud', 'Educación', 'Cultural', 'Infraestructura', 'Asistencia'],
                'datasets': [{
                    'label': 'Programas',
                    'data': programas_radar,
                    'backgroundColor': 'rgba(59, 130, 246, 0.3)',
                    'borderColor': '#3b82f6',
                    'pointBackgroundColor': ['#10b981', '#f59e0b', '#8b5cf6', '#ef4444', '#06b6d4']
                }]
            },
            'proximas_actividades': proximas_actividades_data,
            'autoridades_activas': autoridades_data,
            'evolucion_data': {
                'labels': ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago'],
                'datasets': [{
                    'label': 'Registros',
                    'data': [142, 158, 133, 165, 152, 173, 168, 181],  # Simulado
                    'borderColor': '#3b82f6',
                    'backgroundColor': 'rgba(59, 130, 246, 0.1)',
                    'fill': True,
                    'tension': 0.4,
                    'borderWidth': 2
                }, {
                    'label': 'Meta',
                    'data': [150, 160, 155, 170, 165, 175, 170, 180],  # Simulado
                    'borderColor': '#10b981',
                    'backgroundColor': 'rgba(16, 185, 129, 0.05)',
                    'fill': True,
                    'tension': 0.4,
                    'borderDash': [5, 5],
                    'borderWidth': 2
                }]
            },
            'ocupacion_data': {
                'labels': ['Hombres', 'Mujeres'],
                'datasets': [{
                    'data': [ocupacion_hombres_pct, ocupacion_mujeres_pct],
                    'backgroundColor': ['#3b82f6', '#ec4899'],
                    'borderWidth': 0
                }]
            },
            'desocupacion_data': {
                'labels': ['Hombres', 'Mujeres'],
                'datasets': [{
                    'data': [desocupacion_hombres_pct, desocupacion_mujeres_pct],
                    'backgroundColor': ['#3b82f6', '#ec4899'],
                    'borderWidth': 0
                }]
            },
            'genero_porcentajes': genero_porcentajes,
            'indicadores_data': {
                'labels': ['Alfabetización', 'Empleo', 'Educación', 'Salud', 'Vivienda', 'Servicios'],
                'datasets': [{
                    'data': [tasa_alfabetismo, tasa_empleo, tasa_alfabetismo, 85, 71, 88],  # Salud, Vivienda, Servicios simulados
                    'backgroundColor': ['#8b5cf6', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#6b7280'],
                    'borderWidth': 0
                }]
            },
            'edad_data': {
                'labels': ['0-5', '6-12', '13-17', '18-30', '31-50', '51-65', '65+'],
                'datasets': [{
                    'label': 'Hombres',
                    'backgroundColor': '#3b82f6',
                    'data': edad_hombres
                }, {
                    'label': 'Mujeres',
                    'backgroundColor': '#ec4899',
                    'data': edad_mujeres
                }]
            }
        })

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

    @action(detail=True, methods=['get'])
    def lenguas_por_grupo_etnico(self, request, pk=None):
        """
        Lenguas maternas asociadas a un grupo étnico específico
        """
        try:
            grupo_etnico_id = pk
        except:
            return Response({'error': 'Grupo étnico no especificado'}, status=400)

        # Obtener todas las lenguas maternas de personas que pertenecen a este grupo étnico
        lenguas = Persona.objects.filter(
            grupo_familiar_id=grupo_etnico_id
        ).values('lengua_materna__nombre').annotate(
            count=Count('lengua_materna')
        ).exclude(lengua_materna__isnull=True).order_by('-count')

        data = []
        for lengua in lenguas:
            data.append({
                'id': f"lengua_{lengua['lengua_materna__nombre']}",
                'nombre': lengua['lengua_materna__nombre'],
                'cantidad_hablantes': lengua['count'],
                'tipo': 'lengua_materna'
            })

        return Response(data)

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