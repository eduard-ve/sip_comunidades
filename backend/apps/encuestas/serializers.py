from rest_framework import serializers
from .models import Encuesta, Pregunta, Opcion, Respuesta

# Serializers para los modelos de encuestas
class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id_opcion', 'pregunta', 'texto_opcion', 'valor']

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id_pregunta', 'encuesta', 'texto_pregunta', 'tipo', 'orden', 'opciones']

class EncuestaSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)

    class Meta:
        model = Encuesta
        fields = ['id_encuesta', 'titulo', 'descripcion', 'estado', 'fecha_creacion', 'fecha_cierre', 'preguntas']

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id_respuesta', 'encuesta', 'pregunta', 'opcion', 'respuesta_texto', 'fecha_respuesta']
