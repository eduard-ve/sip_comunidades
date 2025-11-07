from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Modelo para representar una encuesta
class Encuesta(models.Model):
    ESTADO_CHOICES = [
        ('activa', 'Activa'),
        ('cerrada', 'Cerrada'),
        ('borrador', 'Borrador'),
    ]

    id_encuesta = models.BigAutoField(primary_key=True)
    titulo = models.CharField(max_length=255)
    descripcion = models.TextField(blank=True, null=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='borrador')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_cierre = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.titulo

# Modelo para representar una pregunta dentro de una encuesta
class Pregunta(models.Model):
    TIPO_CHOICES = [
        ('opcion_multiple', 'Opción múltiple'),
        ('abierta', 'Abierta'),
        ('escala', 'Escala'),
        ('si_no', 'Sí/No'),
    ]

    id_pregunta = models.BigAutoField(primary_key=True)
    encuesta = models.ForeignKey(Encuesta, related_name='preguntas', on_delete=models.CASCADE)
    texto_pregunta = models.TextField()
    tipo = models.CharField(max_length=20, choices=TIPO_CHOICES)
    orden = models.IntegerField(default=1)

    def __str__(self):
        return self.texto_pregunta

# Modelo para representar una opción de respuesta para preguntas de opción múltiple o escala
class Opcion(models.Model):
    id_opcion = models.BigAutoField(primary_key=True)
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto_opcion = models.CharField(max_length=255)
    valor = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.texto_opcion

# Modelo para representar una respuesta dada por un usuario a una pregunta de una encuesta
class Respuesta(models.Model):
    id_respuesta = models.BigAutoField(primary_key=True)
    encuesta = models.ForeignKey(Encuesta, related_name='respuestas', on_delete=models.CASCADE)
    pregunta = models.ForeignKey(Pregunta, related_name='respuestas', on_delete=models.CASCADE)
    persona = models.ForeignKey('poblacion.Persona', on_delete=models.CASCADE, related_name='respuestas_encuestas', null=True, blank=True)
    opcion = models.ForeignKey(Opcion, blank=True, null=True, on_delete=models.SET_NULL)
    respuesta_texto = models.TextField(blank=True, null=True)
    fecha_respuesta = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Respuesta {self.id_respuesta}"
