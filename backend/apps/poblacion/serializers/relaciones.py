from rest_framework import serializers
from poblacion.models.relaciones import RelacionFamiliar

# Serializer para la relación familiar
class RelacionFamiliarSerializer(serializers.ModelSerializer):
    persona_nombre = serializers.CharField(source='persona.nombre_completo', read_only=True)
    familiar_nombre = serializers.CharField(source='familiar.nombre_completo', read_only=True)
    tipo_relacion_nombre = serializers.CharField(source='tipo_relacion.nombre', read_only=True)

    class Meta:
        model = RelacionFamiliar
        fields = '__all__'