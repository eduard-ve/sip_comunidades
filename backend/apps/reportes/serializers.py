from rest_framework import serializers
from django.db import IntegrityError
from django.db.models import Count
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas
from apps.salud.models import RegistroSalud, AlertaSalud, ControlSalud
from apps.social.models import ProgramaBeneficiario, ActividadSocial
from apps.encuestas.models import Encuesta, Pregunta, Opcion, Respuesta

class ReporteSaludSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSalud
        fields = '__all__'
        read_only_fields = ('generado_por', 'datos_agregados')

    def create(self, validated_data):
        try:
            # Asignar el usuario autenticado como string
            request = self.context.get('request')
            if request and request.user:
                validated_data['generado_por'] = request.user.username

            # Generar datos agregados automáticamente (datos generales del sistema)
            datos_agregados = {
                'total_registros_sistema': RegistroSalud.objects.count(),
                'total_alertas_sistema': AlertaSalud.objects.count(),
                'total_controles_sistema': ControlSalud.objects.count(),
                'alertas_activas_sistema': AlertaSalud.objects.filter(resuelta=False).count(),
                'controles_pendientes_sistema': ControlSalud.objects.filter(realizado=False).count(),
                'estadisticas_generales': {
                    'total_personas': RegistroSalud.objects.values('persona').distinct().count(),
                    'registros_por_tipo': list(RegistroSalud.objects.values('tipo_registro').annotate(count=Count('id'))),
                    'alertas_por_prioridad': list(AlertaSalud.objects.values('prioridad').annotate(count=Count('id')))
                }
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte de salud para este usuario en la misma fecha.'
            })

class ReporteSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteSocial
        fields = '__all__'
        read_only_fields = ('generado_por', 'datos_agregados')

    def create(self, validated_data):
        try:
            # Asignar el usuario autenticado como string
            request = self.context.get('request')
            if request and request.user:
                validated_data['generado_por'] = request.user.username

            # Generar datos agregados automáticamente (datos generales del sistema)
            datos_agregados = {
                'total_programas_sistema': ProgramaBeneficiario.objects.values('programa').distinct().count(),
                'total_beneficiarios_sistema': ProgramaBeneficiario.objects.values('persona').distinct().count(),
                'beneficiarios_activos': ProgramaBeneficiario.objects.filter(estado='activo').values('persona').distinct().count(),
                'programas_por_tipo': list(ProgramaBeneficiario.objects.select_related('programa').values('programa__tipo_programa').annotate(count=Count('programa', distinct=True))),
                'estadisticas_generales': {
                    'total_actividades': ActividadSocial.objects.count(),
                    'actividades_por_programa': list(ProgramaBeneficiario.objects.select_related('programa').values('programa__nombre').annotate(count=Count('id')))
                }
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte social para este usuario en la misma fecha.'
            })

class ReporteEncuestasSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReporteEncuestas
        fields = '__all__'
        read_only_fields = ('generado_por', 'datos_agregados')

    def create(self, validated_data):
        try:
            # Asignar el usuario autenticado como string
            request = self.context.get('request')
            if request and request.user:
                validated_data['generado_por'] = request.user.username

            # Generar datos agregados automáticamente (datos generales del sistema)
            datos_agregados = {
                'encuestas_disponibles': list(Encuesta.objects.filter(estado='activa').values('id_encuesta', 'titulo', 'descripcion')),
                'total_encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
                'total_respuestas_sistema': Respuesta.objects.count(),
                'estadisticas_generales': {
                    'encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
                    'encuestas_cerradas': Encuesta.objects.filter(estado='cerrada').count(),
                    'total_preguntas': Pregunta.objects.count(),
                    'total_opciones': Opcion.objects.count(),
                    'respuestas_por_encuesta': list(Respuesta.objects.values('encuesta__titulo').annotate(count=Count('id_respuesta')))
                }
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte de encuestas para este usuario en la misma fecha.'
            })