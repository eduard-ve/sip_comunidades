from rest_framework import serializers
from ..models import catalogos

# Serializers individuales para cada catálogo
class TipoIdentificacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.TipoIdentificacion
        fields = '__all__'

class NivelEducativoSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.NivelEducativo
        fields = '__all__'

class OcupacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.Ocupacion
        fields = '__all__'

class GrupoFamiliarSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.GrupoFamiliar
        fields = '__all__'

class EstadoCivilSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.EstadoCivil
        fields = '__all__'

class LenguaSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.Lengua
        fields = '__all__'

class TipoRelacionSerializer(serializers.ModelSerializer):
    class Meta:
        model = catalogos.TipoRelacion
        fields = '__all__'

# ViewSet genérico para catálogos
from rest_framework import viewsets, permissions

class CatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]

    # Mapeo de URLs a serializers
    serializer_mapping = {
        'tipos_identificacion': TipoIdentificacionSerializer,
        'niveles_educativos': NivelEducativoSerializer,
        'ocupaciones': OcupacionSerializer,
        'grupos_familiares': GrupoFamiliarSerializer,
        'estados_civiles': EstadoCivilSerializer,
        'lenguas': LenguaSerializer,
        'tipos_relaciones': TipoRelacionSerializer,
    }

    # Mapeo de URLs a modelos
    model_mapping = {
        'tipos_identificacion': 'TipoIdentificacion',
        'niveles_educativos': 'NivelEducativo',
        'ocupaciones': 'Ocupacion',
        'grupos_familiares': 'GrupoFamiliar',
        'estados_civiles': 'EstadoCivil',
        'lenguas': 'Lengua',
        'tipos_relaciones': 'TipoRelacion',
    }

    def get_serializer_class(self):
        """Retorna el serializer correcto según el basename"""
        basename = self.basename
        serializer_class = self.serializer_mapping.get(basename)

        if not serializer_class:
            raise ValueError(f"No serializer found for basename: {basename}")

        return serializer_class

    def get_queryset(self):
        """Retorna el queryset del modelo correcto"""
        basename = self.basename
        model_class_name = self.model_mapping.get(basename)

        if not model_class_name:
            raise ValueError(f"No mapping found for basename: {basename}")

        model_class = getattr(catalogos, model_class_name)
        return model_class.objects.all().order_by('nombre')

class CatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    permission_classes = [permissions.AllowAny]

    # Mapeo de URLs a serializers
    serializer_mapping = {
        'tipos_identificacion': TipoIdentificacionSerializer,
        'niveles_educativos': NivelEducativoSerializer,
        'ocupaciones': OcupacionSerializer,
        'grupos_familiares': GrupoFamiliarSerializer,
        'estados_civiles': EstadoCivilSerializer,
        'lenguas': LenguaSerializer,
        'tipos_relaciones': TipoRelacionSerializer,
    }

    # Mapeo de URLs a modelos
    model_mapping = {
        'tipos_identificacion': 'TipoIdentificacion',
        'niveles_educativos': 'NivelEducativo',
        'ocupaciones': 'Ocupacion',
        'grupos_familiares': 'GrupoFamiliar',
        'estados_civiles': 'EstadoCivil',
        'lenguas': 'Lengua',
        'tipos_relaciones': 'TipoRelacion',
    }

    def get_serializer_class(self):
        """Retorna el serializer correcto según el basename"""
        basename = self.basename
        serializer_class = self.serializer_mapping.get(basename)
        
        if not serializer_class:
            raise ValueError(f"No serializer found for basename: {basename}")
        
        return serializer_class

    def get_queryset(self):
        """Retorna el queryset del modelo correcto"""
        basename = self.basename
        model_class_name = self.model_mapping.get(basename)
        
        if not model_class_name:
            raise ValueError(f"No mapping found for basename: {basename}")

        model_class = getattr(catalogos, model_class_name)
        return model_class.objects.all().order_by('nombre')