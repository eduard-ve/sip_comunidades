from rest_framework import serializers
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas
from apps.salud.models import RegistroSalud, AlertaSalud, ControlSalud
from apps.social.models import ProgramaBeneficiario, ActividadSocial
from apps.encuestas.models import Respuesta

class ReporteSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSalud
        fields = '__all__'

    def create(self, validated_data):
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

class ReporteSocialSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSocial
        fields = '__all__'

    def create(self, validated_data):
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

class ReporteEncuestasSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteEncuestas
        fields = '__all__'

    def create(self, validated_data):
        # Generar datos agregados automáticamente
        persona = validated_data['persona']
        # Nota: Las respuestas no están vinculadas directamente a persona, pero podemos buscar por identificación o similar
        # Por ahora, generamos un reporte básico con estadísticas generales
        datos_agregados = {
            'encuestas_disponibles': list(Encuesta.objects.filter(estado='activa').values('id_encuesta', 'titulo', 'descripcion')),
            'total_encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
            'total_respuestas': Respuesta.objects.count(),  # Nota: Esto es general, no por persona específica
            'estadisticas_generales': {
                'encuestas_activas': Encuesta.objects.filter(estado='activa').count(),
                'encuestas_cerradas': Encuesta.objects.filter(estado='cerrada').count(),
                'total_preguntas': Pregunta.objects.count(),
                'total_opciones': Opcion.objects.count()
            }
        }
        validated_data['datos_agregados'] = datos_agregados
        return super().create(validated_data)