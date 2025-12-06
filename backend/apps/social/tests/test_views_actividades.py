"""
Tests para los ViewSets de actividades comunitarias
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.social.models import TipoActividad, EstadoActividad, ActividadComunitaria, AsistenciaActividad
from apps.poblacion.models.personas import Persona

User = get_user_model()


class TipoActividadViewSetTest(APITestCase):
    """Tests para TipoActividadViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.tipo = TipoActividad.objects.create(
            nombre='Cultural',
            descripcion='Actividades culturales'
        )

    def test_list_tipos_as_admin(self):
        """Test: Listar tipos de actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/tipos-actividad/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_tipo_as_admin(self):
        """Test: Crear tipo de actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nombre': 'Deportiva',
            'descripcion': 'Actividades deportivas'
        }
        response = self.client.post('/api/social/tipos-actividad/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(TipoActividad.objects.count(), 2)

    def test_update_tipo_as_admin(self):
        """Test: Actualizar tipo como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'nombre': 'Cultural Actualizado', 'descripcion': 'Nueva descripción'}
        response = self.client.put(f'/api/social/tipos-actividad/{self.tipo.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.tipo.refresh_from_db()
        self.assertEqual(self.tipo.nombre, 'Cultural Actualizado')

    def test_delete_tipo_as_admin(self):
        """Test: Eliminar tipo como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/tipos-actividad/{self.tipo.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(TipoActividad.objects.count(), 0)


class EstadoActividadViewSetTest(APITestCase):
    """Tests para EstadoActividadViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.estado = EstadoActividad.objects.create(
            nombre='Programada',
            descripcion='Actividad programada',
            color='#007bff'
        )

    def test_list_estados_as_admin(self):
        """Test: Listar estados de actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/estados-actividad/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_estado_as_admin(self):
        """Test: Crear estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'nombre': 'En Curso',
            'descripcion': 'Actividad en curso',
            'color': '#28a745'
        }
        response = self.client.post('/api/social/estados-actividad/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(EstadoActividad.objects.count(), 2)

    def test_update_estado_as_admin(self):
        """Test: Actualizar estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {'nombre': 'Estado Actualizado', 'descripcion': 'Nueva descripción', 'color': '#ff0000'}
        response = self.client.put(f'/api/social/estados-actividad/{self.estado.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.estado.refresh_from_db()
        self.assertEqual(self.estado.nombre, 'Estado Actualizado')

    def test_delete_estado_as_admin(self):
        """Test: Eliminar estado como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/estados-actividad/{self.estado.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(EstadoActividad.objects.count(), 0)


class ActividadComunitariaViewSetTest(APITestCase):
    """Tests para ActividadComunitariaViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.tipo = TipoActividad.objects.create(
            nombre='Cultural',
            descripcion='Actividades culturales'
        )
        self.estado = EstadoActividad.objects.create(
            nombre='Programada',
            descripcion='Actividad programada',
            color='#007bff'
        )
        self.actividad = ActividadComunitaria.objects.create(
            titulo='Actividad Test',
            descripcion='Descripción de la actividad',
            tipo_actividad=self.tipo,
            estado=self.estado,
            fecha_actividad='2024-12-31',
            hora_inicio='10:00:00',
            hora_fin='12:00:00'
        )

    def test_list_actividades_as_admin(self):
        """Test: Listar actividades como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/actividades-comunitarias/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_create_actividad_as_admin(self):
        """Test: Crear actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'titulo': 'Nueva Actividad',
            'descripcion': 'Descripción de la nueva actividad',
            'tipo_actividad': self.tipo.id,
            'estado': self.estado.id,
            'fecha_actividad': '2024-12-31',
            'hora_inicio': '14:00:00',
            'hora_fin': '16:00:00'
        }
        response = self.client.post('/api/social/actividades-comunitarias/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(ActividadComunitaria.objects.count(), 2)

    def test_update_actividad_as_admin(self):
        """Test: Actualizar actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'titulo': 'Actividad Actualizada',
            'descripcion': 'Nueva descripción',
            'tipo_actividad': self.tipo.id,
            'estado': self.estado.id,
            'fecha_actividad': '2024-12-31',
            'hora_inicio': '10:00:00',
            'hora_fin': '12:00:00'
        }
        response = self.client.put(f'/api/social/actividades-comunitarias/{self.actividad.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.actividad.refresh_from_db()
        self.assertEqual(self.actividad.titulo, 'Actividad Actualizada')

    def test_delete_actividad_as_admin(self):
        """Test: Eliminar actividad como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/actividades-comunitarias/{self.actividad.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(ActividadComunitaria.objects.count(), 0)

    def test_registrar_asistencia(self):
        """Test: Registrar asistencia a actividad"""
        self.client.force_authenticate(user=self.admin_user)
        persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        data = {
            'persona_id': persona.id,
            'confirmado': True,
            'observaciones': 'Asistencia confirmada'
        }
        response = self.client.post(
            f'/api/social/actividades-comunitarias/{self.actividad.id}/registrar-asistencia/',
            data
        )
        self.assertIn(response.status_code, [status.HTTP_200_OK, status.HTTP_201_CREATED])
        self.assertTrue(AsistenciaActividad.objects.filter(
            actividad=self.actividad,
            persona=persona
        ).exists())

    def test_registrar_asistencia_sin_persona_id_fails(self):
        """Test: Registrar asistencia sin persona_id falla"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'confirmado': True
        }
        response = self.client.post(
            f'/api/social/actividades-comunitarias/{self.actividad.id}/registrar-asistencia/',
            data
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_estadisticas_actividad(self):
        """Test: Obtener estadísticas de actividad"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get(
            f'/api/social/actividades-comunitarias/{self.actividad.id}/estadisticas/'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_asistentes', response.data)
        self.assertIn('asistentes_confirmados', response.data)


class AsistenciaActividadViewSetTest(APITestCase):
    """Tests para AsistenciaActividadViewSet"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )
        self.tipo = TipoActividad.objects.create(
            nombre='Cultural',
            descripcion='Actividades culturales'
        )
        self.estado = EstadoActividad.objects.create(
            nombre='Programada',
            descripcion='Actividad programada',
            color='#007bff'
        )
        self.actividad = ActividadComunitaria.objects.create(
            titulo='Actividad Test',
            descripcion='Descripción',
            tipo_actividad=self.tipo,
            estado=self.estado,
            fecha_actividad='2024-12-31'
        )
        self.persona = Persona.objects.create(
            nombre='Juan',
            apellido='Pérez',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        self.asistencia = AsistenciaActividad.objects.create(
            actividad=self.actividad,
            persona=self.persona,
            confirmado=True
        )

    def test_list_asistencias_as_admin(self):
        """Test: Listar asistencias como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.get('/api/social/asistencias-actividad/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 1)

    def test_update_asistencia_as_admin(self):
        """Test: Actualizar asistencia como admin"""
        self.client.force_authenticate(user=self.admin_user)
        data = {
            'actividad': self.actividad.id,
            'persona': self.persona.id,
            'confirmado': False,
            'observaciones': 'No asistió'
        }
        response = self.client.put(f'/api/social/asistencias-actividad/{self.asistencia.id}/', data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.asistencia.refresh_from_db()
        self.assertFalse(self.asistencia.confirmado)

    def test_delete_asistencia_as_admin(self):
        """Test: Eliminar asistencia como admin"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.delete(f'/api/social/asistencias-actividad/{self.asistencia.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(AsistenciaActividad.objects.count(), 0)

