from django.test import TestCase
from django.contrib.auth import get_user_model
from .models import Encuesta, Pregunta, Opcion, Respuesta

User = get_user_model()

class EncuestaTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.encuesta = Encuesta.objects.create(titulo="Encuesta Test", descripcion="Descripción", estado="activa")

    def test_encuesta_str(self):
        self.assertEqual(str(self.encuesta), "Encuesta Test")

    def test_crear_pregunta_opcion(self):
        pregunta = Pregunta.objects.create(encuesta=self.encuesta, texto_pregunta="Pregunta 1", tipo="abierta")
        opcion = Opcion.objects.create(pregunta=pregunta, texto_opcion="Opción A", valor=1)
        self.assertEqual(str(pregunta), "Pregunta 1")
        self.assertEqual(str(opcion), "Opción A")
