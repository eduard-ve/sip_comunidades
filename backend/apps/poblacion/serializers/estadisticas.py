from rest_framework import serializers

# Serializers para estadísticas de población
class DistribucionEdadSerializer(serializers.Serializer):
    rango_edad = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

class TopOcupacionSerializer(serializers.Serializer):
    ocupacion = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

class DistribucionEducativaSerializer(serializers.Serializer):
    nivel = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

class LenguaMaternaSerializer(serializers.Serializer):
    lengua = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

class DistribucionGeneroSerializer(serializers.Serializer):
    genero = serializers.CharField()
    cantidad = serializers.IntegerField()
    porcentaje = serializers.FloatField()

class RelacionFamiliarDetailSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    nombre_completo = serializers.CharField()
    relacion = serializers.CharField()
    edad = serializers.IntegerField(allow_null=True)
    ocupacion = serializers.CharField(allow_null=True)