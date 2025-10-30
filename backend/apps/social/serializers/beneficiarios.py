from rest_framework import serializers
from ..models import ProgramaBeneficiario, ActividadSocial, CoberturaPrograma

# Serializers para los modelos relacionados con beneficiarios y actividades sociales
class ProgramaBeneficiarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProgramaBeneficiario
        fields = '__all__'

class ActividadSocialSerializer(serializers.ModelSerializer):
    class Meta:
        model = ActividadSocial
        fields = '__all__'

class CoberturaProgramaSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoberturaPrograma
        fields = '__all__'
