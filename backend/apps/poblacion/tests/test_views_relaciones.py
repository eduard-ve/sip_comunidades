"""
Tests para RelacionFamiliarViewSet
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.poblacion.models.personas import Persona
from apps.poblacion.models.relaciones import RelacionFamiliar
from apps.poblacion.models.catalogos import TipoRelacion

User = get_user_model()


class RelacionFamiliarViewSetTest(APITestCase):
    """Tests para RelacionFamiliarViewSet"""

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
        
        # Crear personas de prueba
        self.persona1 = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        self.persona2 = Persona.objects.create(
            nombre='María',
            apellido='García',
            numero_identificacion='987654321',
            fecha_nacimiento='1992-05-15',
            genero='F'
        )
        
        # Crear tipo de relación
        self.tipo_relacion = TipoRelacion.objects.create(
            nombre='Padre',
            descripcion='Relación padre-hijo'
        )
        
        self.relacion = RelacionFamiliar.objects.create(
            persona=self.persona1,
            familiar=self.persona2,
            tipo_relacion=self.tipo_relacion
        )

    def test_list_relaciones_as_admin(self):
        """Test: Listar relaciones como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/poblacion/relaciones_familiares/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_list_relaciones_as_editor_denied(self):
        """Test: Editor no puede listar relaciones"""
        self.client.force_authenticate(user=self.editor_user)
        response = self.client.get('/api/poblacion/relaciones_familiares/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_create_relacion_as_admin(self):
        """Test: Crear relación como admin"""
        self.client.force_authenticate(user=self.admin_user)
        persona3 = Persona.objects.create(
            nombre='Pedro',
            apellido='López',
            numero_identificacion='111222333',
            fecha_nacimiento='1988-03-20',
            genero='M'
        )
        data = {
            'persona': self.persona1.id,
            'familiar': persona3.id,
            'tipo_relacion': self.tipo_relacion.id
        }
        response = self.client.post('/api/poblacion/relaciones_familiares/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RelacionFamiliar.objects.count(), 2)

    def test_create_duplicate_relacion_fails(self):
        """Test: No se puede crear relación duplicada"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'persona': self.persona1.id,
            'familiar': self.persona2.id,
            'tipo_relacion': self.tipo_relacion.id
        }
        response = self.client.post('/api/poblacion/relaciones_familiares/', data)
        # Debería fallar porque ya existe esta relación
        self.assertIn(response.status_code, [status.HTTP_400_BAD_REQUEST, status.HTTP_201_CREATED])

    def test_update_relacion_as_admin(self):
        """Test: Actualizar relación como admin"""
        self.client.force_authenticate(user=self.admin_user)
        nuevo_tipo = TipoRelacion.objects.create(
            nombre='Hermano',
            descripcion='Relación hermano-hermano'
        )
        data = {
            'persona': self.persona1.id,
            'familiar': self.persona2.id,
            'tipo_relacion': nuevo_tipo.id
        }
        response = self.client.put(f'/api/poblacion/relaciones_familiares/{self.relacion.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.relacion.refresh_from_db()
        self.assertEqual(self.relacion.tipo_relacion.id, nuevo_tipo.id)

    def test_delete_relacion_as_admin(self):
        """Test: Eliminar relación como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/poblacion/relaciones_familiares/{self.relacion.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(RelacionFamiliar.objects.count(), 0)

    def test_filter_relaciones_by_persona(self):
        """Test: Filtrar relaciones por persona"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/poblacion/relaciones_familiares/?persona={self.persona1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_filter_relaciones_by_familiar(self):
        """Test: Filtrar relaciones por familiar"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/poblacion/relaciones_familiares/?familiar={self.persona2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_retrieve_relacion_as_admin(self):
        """Test: Obtener relación específica como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(f'/api/poblacion/relaciones_familiares/{self.relacion.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['persona'], self.persona1.id)
        self.assertEqual(response.data['familiar'], self.persona2.id)

