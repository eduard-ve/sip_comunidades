from rest_framework import serializers
from django.db import IntegrityError
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas
from apps.salud.models import RegistroSalud, AlertaSalud, ControlSalud
from apps.social.models import ProgramaBeneficiario, ActividadSocial
from apps.encuestas.models import Encuesta, Pregunta, Opcion, Respuesta

class ReporteSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSalud
        fields = '__all__'

    def create(self, validated_data):
        try:
            # Generar datos agregados automáticamente
            persona = validated_data['persona']
            datos_agregados = {
                'registros_salud': list(RegistroSalud.objects.filter(persona=persona).values(
                    'id', 'fecha_registro', 'tipo_registro', 'descripcion', 'observaciones'
                )),
                'alertas_salud': list(AlertaSalud.objects.filter(persona=persona).values(
                    'id', 'titulo', 'descripcion', 'prioridad', 'fecha_alerta', 'resuelta'
                )),
                'controles_salud': list(ControlSalud.objects.filter(persona=persona).values(
                    'id', 'tipo_control', 'fecha_programada', 'fecha_realizada', 'realizado', 'observaciones'
                )),
                'total_registros': RegistroSalud.objects.filter(persona=persona).count(),
                'total_alertas': AlertaSalud.objects.filter(persona=persona).count(),
                'total_controles': ControlSalud.objects.filter(persona=persona).count(),
                'alertas_activas': AlertaSalud.objects.filter(persona=persona, resuelta=False).count(),
                'controles_pendientes': ControlSalud.objects.filter(persona=persona, realizado=False).count()
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte de salud para esta persona en la misma fecha.'
            })

class ReporteSocialSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSocial
        fields = '__all__'

    def create(self, validated_data):
        try:
            # Generar datos agregados automáticamente
            persona = validated_data['persona']
            datos_agregados = {
                'programas_beneficiario': list(ProgramaBeneficiario.objects.filter(persona=persona).select_related('programa').values(
                    'id', 'programa__nombre', 'fecha_inscripcion', 'estado', 'observaciones'
                )),
                'actividades_sociales': list(ActividadSocial.objects.filter(programa__beneficiarios=persona).distinct().values(
                    'id', 'titulo', 'descripcion', 'fecha', 'ubicacion', 'programa__nombre'
                )),
                'total_programas': ProgramaBeneficiario.objects.filter(persona=persona).count(),
                'programas_activos': ProgramaBeneficiario.objects.filter(persona=persona, estado='activo').count(),
                'programas_egresados': ProgramaBeneficiario.objects.filter(persona=persona, estado='egresado').count()
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte social para esta persona en la misma fecha.'
            })

class ReporteEncuestasSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteEncuestas
        fields = '__all__'

    def create(self, validated_data):
        try:
            # Generar datos agregados automáticamente
            persona = validated_data['persona']
            # Obtener respuestas de la persona específica
            respuestas_persona = Respuesta.objects.filter(persona=persona, encuesta__estado='activa')

            datos_agregados = {
                'encuestas_disponibles': list(Encuesta.objects.filter(estado='activa').values('id_encuesta', 'titulo', 'descripcion')),
                'total_encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
                'total_respuestas_persona': respuestas_persona.count(),
                'respuestas_detalladas': list(respuestas_persona.values(
                    'id_respuesta', 'encuesta__titulo', 'pregunta__texto_pregunta',
                    'opcion__texto_opcion', 'respuesta_texto', 'fecha_respuesta'
                )),
                'estadisticas_generales': {
                    'encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
                    'encuestas_cerradas': Encuesta.objects.filter(estado='cerrada').count(),
                    'total_preguntas': Pregunta.objects.count(),
                    'total_opciones': Opcion.objects.count()
                }
            }
            validated_data['datos_agregados'] = datos_agregados
            return super().create(validated_data)
        except IntegrityError:
            raise serializers.ValidationError({
                'error': 'Ya existe un reporte de encuestas para esta persona en la misma fecha.'
            })