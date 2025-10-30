from rest_framework import serializers
from .models import RegistroSalud, AlertaSalud, ControlSalud

class RegistroSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = RegistroSalud
        fields = '__all__'

class AlertaSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = AlertaSalud
        fields = '__all__'

class ControlSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ControlSalud
        fields = '__all__'