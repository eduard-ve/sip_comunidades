# cargar_encuestas.py
from apps.encuestas.models import Encuesta, Pregunta, Opcion
from django.contrib.auth import get_user_model
from datetime import datetime

User = get_user_model()

# Obtener un usuario existente para asignar la encuesta
usuario = User.objects.first()
if not usuario:
    raise Exception("No hay usuarios en la base de datos. Crea uno primero.")

# Crear una encuesta
encuesta = Encuesta.objects.create(
    titulo="Encuesta de Satisfacción",
    descripcion="Encuesta inicial para probar el sistema",
    estado="activa",
    fecha_creacion=datetime.now()
)

# Crear preguntas
pregunta1 = Pregunta.objects.create(
    encuesta=encuesta,
    texto_pregunta="¿Qué tan satisfecho estás con el sistema?",
    tipo="escala",
    orden=1
)

pregunta2 = Pregunta.objects.create(
    encuesta=encuesta,
    texto_pregunta="¿Qué mejorarías en el sistema?",
    tipo="abierta",
    orden=2
)

pregunta3 = Pregunta.objects.create(
    encuesta=encuesta,
    texto_pregunta="¿Recomendarías este sistema a otros?",
    tipo="si_no",
    orden=3
)

# Crear opciones para la pregunta de escala
Opcion.objects.create(pregunta=pregunta1, texto_opcion="Muy insatisfecho", valor=1)
Opcion.objects.create(pregunta=pregunta1, texto_opcion="Insatisfecho", valor=2)
Opcion.objects.create(pregunta=pregunta1, texto_opcion="Neutral", valor=3)
Opcion.objects.create(pregunta=pregunta1, texto_opcion="Satisfecho", valor=4)
Opcion.objects.create(pregunta=pregunta1, texto_opcion="Muy satisfecho", valor=5)

print("Encuesta inicial creada con éxito:")
print(f"Encuesta: {encuesta.titulo}")
print("Preguntas:")
for p in encuesta.preguntas.all():
    print(f"- {p.texto_pregunta}")
