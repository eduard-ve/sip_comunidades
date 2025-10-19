from rest_framework import serializers
from poblacion.models.catalogos import (
    TipoIdentificacion, NivelEducatico, Ocupacion, 
    GrupoFamiliar, EstadoCivil, Lengua, TipoRelacion
)

class CatalogoBaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # será asignado dinámicamente en las vistas
        fields = ['id', 'nombre']