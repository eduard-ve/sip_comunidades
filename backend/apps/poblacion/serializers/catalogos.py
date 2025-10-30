from rest_framework import serializers
from ..models.catalogos import (
    TipoIdentificacion, NivelEducativo, Ocupacion,
    GrupoFamiliar, EstadoCivil, Lengua, TipoRelacion
)

class CatalogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = None  # será asignado dinámicamente en las vistas
        fields = ['id', 'nombre']