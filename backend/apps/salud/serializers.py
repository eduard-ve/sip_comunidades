from rest_framework import serializers
from .models import RegistroSalud, AlertaSalud, ControlSalud, HistorialMedico, Vacuna, Medicamento, ExamenMedico

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
        fields = ['id', 'persona', 'titulo', 'descripcion', 'prioridad', 'fecha_alerta', 'resuelta', 'fecha_resolucion', 'fecha_creacion', 'fecha_modificacion', 'persona_nombre', 'persona_apellido', 'persona_identificacion']
        extra_kwargs = {
            'persona': {'required': False}
        }

class ControlSaludSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ControlSalud
        fields = '__all__'

class HistorialMedicoSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = HistorialMedico
        fields = '__all__'

class VacunaSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = Vacuna
        fields = '__all__'

class MedicamentoSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = Medicamento
        fields = '__all__'

class ExamenMedicoSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.primer_nombre', read_only=True)
    persona_apellido = serializers.CharField(source='persona.primer_apellido', read_only=True)
    persona_identificacion = serializers.CharField(source='persona.numero_identificacion', read_only=True)

    class Meta:
        model = ExamenMedico
        fields = '__all__'