from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from apps.poblacion.models.personas import Persona
from apps.poblacion.models.catalogos import TipoIdentificacion
from .models import RegistroSalud, AlertaSalud, ControlSalud

Usuario = get_user_model()

class SaludModuloTests(APITestCase):
    def setUp(self):
        # Crear usuario admin
        self.admin = Usuario.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Admin123!",
            rol=Usuario.ADMIN,
            is_staff=True
        )

        # Crear tipo de identificación
        self.tipo_id = TipoIdentificacion.objects.create(nombre="Cédula")

        # Crear persona de prueba
        self.persona = Persona.objects.create(
            tipo_identificacion=self.tipo_id,
            numero_identificacion="123456789",
            primer_nombre="Juan",
            primer_apellido="Pérez",
            fecha_nacimiento="1990-01-01",
            genero="M"
        )

        # Endpoints
        self.registros_url = reverse('registros-salud-list')
        self.alertas_url = reverse('alertas-salud-list')
        self.controles_url = reverse('controles-salud-list')

        # Token para autenticación
        self.token = RefreshToken.for_user(self.admin).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    # -----------------------
    # Registros de Salud
    # -----------------------
    def test_crear_registro_salud(self):
        """Crear un registro de salud válido"""
        data = {
            "persona": self.persona.id,
            "tipo_registro": "Consulta médica",
            "fecha_registro": "2024-01-15",
            "descripcion": "Consulta general",
            "observaciones": "Paciente en buen estado"
        }
        response = self.client.post(self.registros_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(RegistroSalud.objects.filter(persona=self.persona).exists())

    def test_listar_registros_salud(self):
        """Listar registros de salud"""
        RegistroSalud.objects.create(
            persona=self.persona,
            tipo_registro="Vacunación",
            fecha_registro="2024-01-10"
        )
        response = self.client.get(self.registros_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_actualizar_registro_salud(self):
        """Actualizar un registro de salud"""
        registro = RegistroSalud.objects.create(
            persona=self.persona,
            tipo_registro="Consulta",
            fecha_registro="2024-01-01"
        )
        data = {"observaciones": "Actualización de observaciones"}
        response = self.client.patch(f"{self.registros_url}{registro.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        registro.refresh_from_db()
        self.assertEqual(registro.observaciones, "Actualización de observaciones")

    # -----------------------
    # Alertas de Salud
    # -----------------------
    def test_crear_alerta_salud(self):
        """Crear una alerta de salud"""
        data = {
            "persona": self.persona.id,
            "titulo": "Alerta médica",
            "descripcion": "Requiere atención inmediata",
            "prioridad": "alta"
        }
        response = self.client.post(self.alertas_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(AlertaSalud.objects.filter(persona=self.persona).exists())

    def test_marcar_alerta_resuelta(self):
        """Marcar alerta como resuelta"""
        alerta = AlertaSalud.objects.create(
            persona=self.persona,
            titulo="Alerta de prueba",
            descripcion="Descripción de prueba",
            prioridad="media"
        )
        data = {"resuelta": True, "fecha_resolucion": "2024-01-20"}
        response = self.client.patch(f"{self.alertas_url}{alerta.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        alerta.refresh_from_db()
        self.assertTrue(alerta.resuelta)

    def test_filtrar_alertas_por_prioridad(self):
        """Filtrar alertas por prioridad"""
        AlertaSalud.objects.create(
            persona=self.persona,
            titulo="Alerta baja",
            descripcion="Descripción",
            prioridad="baja"
        )
        AlertaSalud.objects.create(
            persona=self.persona,
            titulo="Alerta alta",
            descripcion="Descripción",
            prioridad="alta"
        )
        response = self.client.get(self.alertas_url, {"prioridad": "alta"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verificar que solo retorna alertas de alta prioridad

    # -----------------------
    # Controles de Salud
    # -----------------------
    def test_crear_control_salud(self):
        """Crear un control de salud"""
        data = {
            "persona": self.persona.id,
            "tipo_control": "Chequeo anual",
            "fecha_programada": "2024-06-15",
            "observaciones": "Control rutinario"
        }
        response = self.client.post(self.controles_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(ControlSalud.objects.filter(persona=self.persona).exists())

    def test_marcar_control_realizado(self):
        """Marcar control como realizado"""
        control = ControlSalud.objects.create(
            persona=self.persona,
            tipo_control="Vacunación",
            fecha_programada="2024-02-01"
        )
        data = {"realizado": True, "fecha_realizada": "2024-02-01"}
        response = self.client.patch(f"{self.controles_url}{control.id}/", data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        control.refresh_from_db()
        self.assertTrue(control.realizado)

    def test_eliminar_registro_salud(self):
        """Eliminar un registro de salud"""
        registro = RegistroSalud.objects.create(
            persona=self.persona,
            tipo_registro="Consulta",
            fecha_registro="2024-01-01"
        )
        response = self.client.delete(f"{self.registros_url}{registro.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(RegistroSalud.objects.filter(id=registro.id).exists())

    # -----------------------
    # Serialización y campos relacionados
    # -----------------------
    def test_serializacion_incluye_datos_persona(self):
        """Verificar que la serialización incluye datos de la persona"""
        registro = RegistroSalud.objects.create(
            persona=self.persona,
            tipo_registro="Consulta",
            fecha_registro="2024-01-01"
        )
        response = self.client.get(f"{self.registros_url}{registro.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("persona_nombre", response.data)
        self.assertEqual(response.data["persona_nombre"], "Juan")

    # -----------------------
    # Validaciones
    # -----------------------
    def test_registro_sin_persona_falla(self):
        """Crear registro sin persona debe fallar"""
        data = {
            "tipo_registro": "Consulta",
            "fecha_registro": "2024-01-15"
        }
        response = self.client.post(self.registros_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_alerta_prioridad_invalida_falla(self):
        """Prioridad inválida debe fallar"""
        data = {
            "persona": self.persona.id,
            "titulo": "Alerta",
            "descripcion": "Descripción",
            "prioridad": "invalida"
        }
        response = self.client.post(self.alertas_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
