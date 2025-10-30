from rest_framework import serializers
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas

class ReporteSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSalud
        fields = '__all__'

class ReporteSocialSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteSocial
        fields = '__all__'

class ReporteEncuestasSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ReporteEncuestas
        fields = '__all__'