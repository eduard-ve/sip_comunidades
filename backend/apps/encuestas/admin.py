from django.contrib import admin
from .models import Encuesta, Pregunta, Opcion, Respuesta

# Registro de los modelos en el admin de Django
admin.site.register(Encuesta)
admin.site.register(Pregunta)
admin.site.register(Opcion)
admin.site.register(Respuesta)