"""
Tests para los ViewSets de programas sociales
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.social.models import EstadoPrograma, ProgramaSocial
from apps.poblacion.models.personas import Persona

User = get_user_model()


class EstadoProgramaViewSetTest(APITestCase):
    """Tests para EstadoProgramaViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.editor_user = User.objects.create_user(
            username='editor',
            email='editor@test.com',
            password='testpass123',
            rol='editor'
        )
        self.estado = EstadoPrograma.objects.create(
            nombre='Activo',
            descripcion='Programa activo',
            color='#28a745'
        )

    def test_list_estados_as_admin(self):
        """Test: Listar estados como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/estados/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_estados_as_editor_denied(self):
        """Test: Editor no puede listar estados"""
        self.client.force_authenticate(user=self.editor_user)
        response = self.client.get('/api/social/estados/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_estado_as_admin(self):
        """Test: Crear estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nombre': 'Nuevo Estado',
            'descripcion': 'Descripción del estado',
            'color': '#007bff'
        }
        response = self.client.post('/api/social/estados/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EstadoPrograma.objects.count(), 2)

    def test_update_estado_as_admin(self):
        """Test: Actualizar estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'nombre': 'Estado Actualizado', 'descripcion': 'Nueva descripción', 'color': '#ff0000'}
        response = self.client.put(f'/api/social/estados/{self.estado.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estado.refresh_from_db()
        self.assertEqual(self.estado.nombre, 'Estado Actualizado')

    def test_delete_estado_as_admin(self):
        """Test: Eliminar estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/estados/{self.estado.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EstadoPrograma.objects.count(), 0)


class ProgramaSocialViewSetTest(APITestCase):
    """Tests para ProgramaSocialViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.estado = EstadoPrograma.objects.create(
            nombre='Activo',
            descripcion='Programa activo',
            color='#28a745'
        )
        self.programa = ProgramaSocial.objects.create(
            nombre='Programa Test',
            descripcion='Descripción del programa',
            estado=self.estado,
            fecha_inicio='2024-01-01',
            fecha_fin='2024-12-31'
        )

    def test_list_programas_as_admin(self):
        """Test: Listar programas como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/programas/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_programa_as_admin(self):
        """Test: Crear programa como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nombre': 'Nuevo Programa',
            'descripcion': 'Descripción del nuevo programa',
            'estado': self.estado.id,
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-12-31'
        }
        response = self.client.post('/api/social/programas/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ProgramaSocial.objects.count(), 2)

    def test_update_programa_as_admin(self):
        """Test: Actualizar programa como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nombre': 'Programa Actualizado',
            'descripcion': 'Nueva descripción',
            'estado': self.estado.id,
            'fecha_inicio': '2024-01-01',
            'fecha_fin': '2024-12-31'
        }
        response = self.client.put(f'/api/social/programas/{self.programa.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.programa.refresh_from_db()
        self.assertEqual(self.programa.nombre, 'Programa Actualizado')

    def test_delete_programa_as_admin(self):
        """Test: Eliminar programa como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/programas/{self.programa.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ProgramaSocial.objects.count(), 0)

    def test_filter_programas_by_estado(self):
        """Test: Filtrar programas por estado"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/social/programas/?estado={self.estado.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

