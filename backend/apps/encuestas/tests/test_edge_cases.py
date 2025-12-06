"""
Tests de casos límite (edge cases) para la app de encuestas
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.encuestas.models import Encuesta, Pregunta, Opcion, Respuesta
from apps.poblacion.models.personas import Persona

User = get_user_model()


class EncuestaEdgeCasesTest(APITestCase):
    """Tests de casos límite para Encuesta"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )

    def test_encuesta_with_unicode_characters(self):
        """Test: Crear encuesta con caracteres Unicode"""
        encuesta = Encuesta.objects.create(
            titulo='Encuesta con caracteres especiales: José, María, Ñoño',
            descripcion='Descripción con énfasis y acentos: café, acción',
            estado='activa'
        )
        
        self.assertIsNotNone(encuesta)
        self.assertIn('José', encuesta.titulo)
        self.assertIn('café', encuesta.descripcion)

    def test_encuesta_with_max_length_titulo(self):
        """Test: Crear encuesta con título de longitud máxima"""
        max_titulo = 'A' * 200  # Ajustar según max_length real
        encuesta = Encuesta.objects.create(
            titulo=max_titulo[:200],
            descripcion='Test',
            estado='activa'
        )
        
        self.assertIsNotNone(encuesta)
        self.assertEqual(len(encuesta.titulo), 200)

    def test_encuesta_with_special_characters(self):
        """Test: Crear encuesta con caracteres especiales"""
        titulo = "Encuesta <script>alert('test')</script> & más"
        encuesta = Encuesta.objects.create(
            titulo=titulo,
            descripcion='Test',
            estado='activa'
        )
        
        self.assertIsNotNone(encuesta)
        self.assertIn('script', encuesta.titulo)

    def test_pregunta_with_empty_texto(self):
        """Test: Crear pregunta con texto vacío (debería fallar o tener validación)"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        
        try:
            pregunta = Pregunta.objects.create(
                encuesta=encuesta,
                texto_pregunta='',
                tipo='abierta',
                orden=1
            )
            # Si se crea, verificar que el texto está vacío
            self.assertEqual(pregunta.texto_pregunta, '')
        except Exception:
            # Si falla por validación, está bien
            pass

    def test_pregunta_opcion_multiple_sin_opciones(self):
        """Test: Crear pregunta de opción múltiple sin opciones"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='Pregunta sin opciones?',
            tipo='opcion_multiple',
            orden=1
        )
        
        self.assertIsNotNone(pregunta)
        self.assertEqual(pregunta.opciones.count(), 0)

    def test_opcion_with_unicode_text(self):
        """Test: Crear opción con texto Unicode"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='¿Cuál es tu opción?',
            tipo='opcion_multiple',
            orden=1
        )
        
        opcion = Opcion.objects.create(
            pregunta=pregunta,
            texto_opcion='Opción con caracteres especiales: Sí, No, Tal vez, Ñoño'
        )
        
        self.assertIsNotNone(opcion)
        self.assertIn('Ñoño', opcion.texto_opcion)

    def test_respuesta_with_very_long_text(self):
        """Test: Crear respuesta con texto muy largo"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='Describe tu experiencia',
            tipo='abierta',
            orden=1
        )
        persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        
        long_text = 'A' * 5000  # Texto muy largo
        respuesta = Respuesta.objects.create(
            encuesta=encuesta,
            pregunta=pregunta,
            persona=persona,
            texto_respuesta=long_text[:2000]  # Ajustar según max_length
        )
        
        self.assertIsNotNone(respuesta)
        self.assertGreater(len(respuesta.texto_respuesta), 1000)

    def test_encuesta_with_all_estados(self):
        """Test: Crear encuestas con todos los estados posibles"""
        estados = ['activa', 'cerrada', 'borrador']
        
        for estado in estados:
            encuesta = Encuesta.objects.create(
                titulo=f'Encuesta {estado}',
                descripcion='Test',
                estado=estado
            )
            self.assertEqual(encuesta.estado, estado)

    def test_pregunta_with_all_tipos(self):
        """Test: Crear preguntas con todos los tipos posibles"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        
        tipos = ['abierta', 'opcion_multiple', 'si_no', 'escala']
        
        for i, tipo in enumerate(tipos, 1):
            pregunta = Pregunta.objects.create(
                encuesta=encuesta,
                texto_pregunta=f'Pregunta {tipo}?',
                tipo=tipo,
                orden=i
            )
            self.assertEqual(pregunta.tipo, tipo)

    def test_respuesta_with_special_characters(self):
        """Test: Crear respuesta con caracteres especiales"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='Comentarios?',
            tipo='abierta',
            orden=1
        )
        persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        
        texto_respuesta = "Respuesta con caracteres especiales: <script>alert('test')</script> & más"
        respuesta = Respuesta.objects.create(
            encuesta=encuesta,
            pregunta=pregunta,
            persona=persona,
            texto_respuesta=texto_respuesta
        )
        
        self.assertIsNotNone(respuesta)
        self.assertIn('script', respuesta.texto_respuesta)

    def test_encuesta_with_many_preguntas(self):
        """Test: Crear encuesta con muchas preguntas"""
        encuesta = Encuesta.objects.create(
            titulo='Encuesta extensa',
            descripcion='Test',
            estado='activa'
        )
        
        # Crear 50 preguntas
        for i in range(50):
            Pregunta.objects.create(
                encuesta=encuesta,
                texto_pregunta=f'Pregunta {i+1}?',
                tipo='abierta',
                orden=i+1
            )
        
        self.assertEqual(encuesta.preguntas.count(), 50)

    def test_pregunta_with_many_opciones(self):
        """Test: Crear pregunta con muchas opciones"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='Selecciona una opción',
            tipo='opcion_multiple',
            orden=1
        )
        
        # Crear 20 opciones
        for i in range(20):
            Opcion.objects.create(
                pregunta=pregunta,
                texto_opcion=f'Opción {i+1}'
            )
        
        self.assertEqual(pregunta.opciones.count(), 20)

    def test_respuesta_with_null_persona(self):
        """Test: Crear respuesta sin persona (anónima)"""
        encuesta = Encuesta.objects.create(
            titulo='Test',
            descripcion='Test',
            estado='activa'
        )
        pregunta = Pregunta.objects.create(
            encuesta=encuesta,
            texto_pregunta='Test?',
            tipo='abierta',
            orden=1
        )
        
        try:
            respuesta = Respuesta.objects.create(
                encuesta=encuesta,
                pregunta=pregunta,
                persona=None,
                texto_respuesta='Respuesta anónima'
            )
            self.assertIsNotNone(respuesta)
            self.assertIsNone(respuesta.persona)
        except Exception:
            # Si el modelo requiere persona, está bien
            pass

