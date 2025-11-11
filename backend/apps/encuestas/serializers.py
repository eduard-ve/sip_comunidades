from rest_framework import serializers
from .models import Encuesta, Pregunta, Opcion, Respuesta

# Serializers para los modelos de encuestas
class OpcionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['id_opcion', 'pregunta', 'texto_opcion', 'valor']

class OpcionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Opcion
        fields = ['texto_opcion', 'valor']

    def validate_texto_opcion(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El texto de la opción no puede estar vacío")
        return value.strip()

    def validate_valor(self, value):
        if value is not None and not isinstance(value, (int, float)):
            raise serializers.ValidationError("El valor debe ser un número")
        return value

class PreguntaSerializer(serializers.ModelSerializer):
    opciones = OpcionSerializer(many=True, read_only=True)

    class Meta:
        model = Pregunta
        fields = ['id_pregunta', 'texto_pregunta', 'tipo', 'orden', 'opciones']

class PreguntaCreateSerializer(serializers.ModelSerializer):
    opciones = OpcionCreateSerializer(many=True, required=False, allow_empty=True)

    class Meta:
        model = Pregunta
        fields = ['texto_pregunta', 'tipo', 'orden', 'opciones']

    def validate_texto_pregunta(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El texto de la pregunta no puede estar vacío")
        return value.strip()

    def validate_tipo(self, value):
        tipos_validos = ['abierta', 'opcion_multiple', 'si_no', 'escala']
        if value not in tipos_validos:
            raise serializers.ValidationError(f"Tipo de pregunta inválido. Debe ser uno de: {', '.join(tipos_validos)}")
        return value

    def validate(self, data):
        tipo = data.get('tipo')
        opciones = data.get('opciones', [])

        # Validaciones específicas por tipo
        if tipo in ['opcion_multiple', 'escala'] and not opciones:
            raise serializers.ValidationError(f"Las preguntas de tipo '{tipo}' requieren al menos una opción")

        if tipo == 'si_no' and len(opciones) != 2:
            # Para si_no, asegurar que tenga exactamente 2 opciones si se proporcionan
            pass  # Permitir que se creen automáticamente en el frontend

        return data

class EncuestaSerializer(serializers.ModelSerializer):
    preguntas = PreguntaSerializer(many=True, read_only=True)
    respuestas_count = serializers.ReadOnlyField()

    class Meta:
        model = Encuesta
        fields = ['id_encuesta', 'titulo', 'descripcion', 'estado', 'fecha_creacion', 'fecha_cierre', 'preguntas', 'respuestas_count']

class EncuestaCreateSerializer(serializers.ModelSerializer):
    preguntas = PreguntaCreateSerializer(many=True, required=True, allow_empty=False)

    class Meta:
        model = Encuesta
        fields = ['titulo', 'descripcion', 'estado', 'preguntas']

    def validate_titulo(self, value):
        if not value or not value.strip():
            raise serializers.ValidationError("El título de la encuesta no puede estar vacío")
        if len(value.strip()) < 3:
            raise serializers.ValidationError("El título debe tener al menos 3 caracteres")
        return value.strip()

    def validate_estado(self, value):
        estados_validos = ['activa', 'cerrada', 'borrador']
        if value not in estados_validos:
            raise serializers.ValidationError(f"Estado inválido. Debe ser uno de: {', '.join(estados_validos)}")
        return value

    def validate(self, data):
        preguntas = data.get('preguntas', [])
        if not preguntas:
            raise serializers.ValidationError("La encuesta debe tener al menos una pregunta")

        # Validar que no haya preguntas duplicadas
        textos_preguntas = [p['texto_pregunta'] for p in preguntas]
        if len(textos_preguntas) != len(set(textos_preguntas)):
            raise serializers.ValidationError("No se permiten preguntas duplicadas en la misma encuesta")

        return data

    def create(self, validated_data):
        try:
            preguntas_data = validated_data.pop('preguntas', [])
            encuesta = Encuesta.objects.create(**validated_data)

            for pregunta_data in preguntas_data:
                opciones_data = pregunta_data.pop('opciones', [])
                pregunta = Pregunta.objects.create(encuesta=encuesta, **pregunta_data)

                for opcion_data in opciones_data:
                    Opcion.objects.create(pregunta=pregunta, **opcion_data)

            return encuesta
        except Exception as e:
            # Si hay error, limpiar la encuesta creada parcialmente
            if 'encuesta' in locals():
                try:
                    encuesta.delete()
                except:
                    pass
            raise serializers.ValidationError(f"Error al crear la encuesta: {str(e)}")

class RespuestaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Respuesta
        fields = ['id_respuesta', 'encuesta', 'pregunta', 'opcion', 'respuesta_texto', 'fecha_respuesta']
