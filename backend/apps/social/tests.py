from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from datetime import date

from .models import EstadoPrograma, ProgramaSocial, ProgramaBeneficiario, ActividadSocial, CoberturaPrograma
from apps.poblacion.models import personas
from apps.poblacion.models.catalogos import TipoIdentificacion
from apps.usuarios.models import Usuario

Usuario = get_user_model()

class SocialModuloTests(APITestCase):
    def setUp(self):
        # Crear usuario admin para autenticación
        self.admin = Usuario.objects.create_superuser(
            username="admin_social",
            email="admin_social@example.com",
            password="Admin123!",
            rol=Usuario.ADMIN,
            is_staff=True
        )

        # Crear tipo de identificación para personas
        self.tipo_id = TipoIdentificacion.objects.create(nombre="Cédula")

        # Crear estado de programa
        self.estado = EstadoPrograma.objects.create(nombre="Activo")

        # Crear persona para beneficiarios
        self.persona = personas.Persona.objects.create(
            tipo_identificacion=self.tipo_id,
            numero_identificacion="123456789",
            primer_nombre="Juan",
            primer_apellido="Pérez",
            fecha_nacimiento=date(1990, 1, 1),
            genero="M"
        )

        # Crear programa social
        self.programa = ProgramaSocial.objects.create(
            nombre="Programa de Alimentación",
            descripcion="Programa para apoyar alimentación",
            estado=self.estado,
            fecha_inicio=date(2023, 1, 1),
            responsable=self.admin
        )

        # URLs de la API
        self.estados_url = reverse('social:estado-list')
        self.programas_url = reverse('social:programa-list')
        self.beneficiarios_url = reverse('social:beneficiario-list')
        self.actividades_url = reverse('social:actividad-list')
        self.coberturas_url = reverse('social:cobertura-list')


        # Token para autenticación
        self.token = RefreshToken.for_user(self.admin).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

    # -----------------------
    # Tests de Modelos
    # -----------------------
    def test_creacion_estado_programa(self):
        """Verificar creación de EstadoPrograma"""
        estado = EstadoPrograma.objects.create(nombre="Inactivo")
        self.assertEqual(estado.nombre, "Inactivo")
        self.assertEqual(str(estado), "Inactivo")

    def test_creacion_programa_social(self):
        """Verificar creación de ProgramaSocial con relaciones"""
        programa = ProgramaSocial.objects.create(
            nombre="Programa Educativo",
            descripcion="Programa para educación",
            estado=self.estado,
            responsable=self.admin
        )
        self.assertEqual(programa.nombre, "Programa Educativo")
        self.assertEqual(programa.estado, self.estado)
        self.assertEqual(programa.responsable, self.admin)

    def test_relacion_programa_beneficiario(self):
        """Verificar relación ProgramaBeneficiario"""
        beneficiario = ProgramaBeneficiario.objects.create(
            programa=self.programa,
            persona=self.persona,
            observaciones="Beneficiario activo"
        )
        self.assertEqual(beneficiario.programa, self.programa)
        self.assertEqual(beneficiario.persona, self.persona)
        self.assertEqual(beneficiario.estado, 'activo')

    def test_creacion_actividad_social(self):
        """Verificar creación de ActividadSocial"""
        actividad = ActividadSocial.objects.create(
            programa=self.programa,
            titulo="Taller de Nutrición",
            descripcion="Taller sobre alimentación saludable",
            fecha=date(2023, 6, 15),
            ubicacion="Centro Comunitario"
        )
        self.assertEqual(actividad.titulo, "Taller de Nutrición")
        self.assertEqual(actividad.programa, self.programa)

    def test_creacion_cobertura_programa(self):
        """Verificar creación de CoberturaPrograma"""
        cobertura = CoberturaPrograma.objects.create(
            programa=self.programa,
            latitud=4.6097,
            longitud=-74.0817,
            descripcion="Cobertura en Bogotá",
            area_nombre="Centro"
        )
        self.assertEqual(cobertura.programa, self.programa)
        self.assertEqual(float(cobertura.latitud), 4.6097)
        self.assertEqual(float(cobertura.longitud), -74.0817)

    # -----------------------
    # Tests de API - EstadoPrograma
    # -----------------------
    def test_listar_estados_programa(self):
        """Listar todos los estados de programa"""
        response = self.client.get(self.estados_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_estado_programa(self):
        """Crear nuevo estado de programa"""
        data = {"nombre": "Suspendido"}
        response = self.client.post(self.estados_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], "Suspendido")

    def test_detalle_estado_programa(self):
        """Obtener detalle de estado de programa"""
        url = reverse('social:estado-detail', kwargs={'pk': self.estado.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Activo")

    # -----------------------
    # Tests de API - ProgramaSocial
    # -----------------------
    def test_listar_programas_sociales(self):
        """Listar todos los programas sociales"""
        response = self.client.get(self.programas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_crear_programa_social(self):
        """Crear nuevo programa social"""
        data = {
            "nombre": "Programa de Salud",
            "descripcion": "Programa para atención médica",
            "estado_id": self.estado.id,
            "fecha_inicio": "2023-02-01",
            "responsable": self.admin.id
        }
        response = self.client.post(self.programas_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['nombre'], "Programa de Salud")

    def test_detalle_programa_social(self):
        """Obtener detalle de programa social"""
        url = reverse('social:programa-detail', kwargs={'pk': self.programa.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nombre'], "Programa de Alimentación")

    # -----------------------
    # Tests de API - ProgramaBeneficiario
    # -----------------------
    def test_listar_beneficiarios(self):
        """Listar todos los beneficiarios"""
        response = self.client.get(self.beneficiarios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_beneficiario(self):
        """Crear nuevo beneficiario"""
        data = {
            "programa": self.programa.id,
            "persona": self.persona.id,
            "observaciones": "Nuevo beneficiario"
        }
        response = self.client.post(self.beneficiarios_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['programa'], self.programa.id)

    # -----------------------
    # Tests de API - ActividadSocial
    # -----------------------
    def test_listar_actividades(self):
        """Listar todas las actividades sociales"""
        response = self.client.get(self.actividades_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_actividad_social(self):
        """Crear nueva actividad social"""
        data = {
            "titulo": "Charla Motivacional",
            "descripcion": "Charla sobre emprendimiento",
            "fecha": "2023-07-20",
            "ubicacion": "Auditorio Principal",
            "programa": self.programa.id
        }
        response = self.client.post(self.actividades_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['titulo'], "Charla Motivacional")

    # -----------------------
    # Tests de API - CoberturaPrograma
    # -----------------------
    def test_listar_coberturas(self):
        """Listar todas las coberturas de programa"""
        response = self.client.get(self.coberturas_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_crear_cobertura_programa(self):
        """Crear nueva cobertura de programa"""
        data = {
            "programa": self.programa.id,
            "latitud": 4.7110,
            "longitud": -74.0721,
            "descripcion": "Cobertura en Chapinero",
            "area_nombre": "Chapinero"
        }
        response = self.client.post(self.coberturas_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['area_nombre'], "Chapinero")

    # -----------------------
    # Tests de Integración
    # -----------------------
    def test_integracion_programa_beneficiarios(self):
        """Verificar integración entre programa y beneficiarios"""
        # Crear beneficiario
        beneficiario = ProgramaBeneficiario.objects.create(
            programa=self.programa,
            persona=self.persona
        )

        # Verificar que el programa tiene el beneficiario
        self.assertIn(self.persona, self.programa.beneficiarios.all())

        # Verificar que la persona tiene el programa
        self.assertIn(self.programa, self.persona.programas_sociales.all())

    def test_integracion_con_usuarios(self):
        """Verificar integración con módulo de usuarios"""
        # El responsable del programa debe ser un usuario válido
        self.assertEqual(self.programa.responsable, self.admin)
        self.assertIsInstance(self.programa.responsable, Usuario)

    def test_integracion_con_poblacion(self):
        """Verificar integración con módulo de población"""
        # Los beneficiarios deben ser personas válidas
        beneficiario = ProgramaBeneficiario.objects.create(
            programa=self.programa,
            persona=self.persona
        )
        self.assertIsInstance(beneficiario.persona, personas.Persona)
        self.assertEqual(beneficiario.persona.numero_identificacion, "123456789")
