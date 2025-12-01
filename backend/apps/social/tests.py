import pytest
from django.urls import reverse
from rest_framework import status
from datetime import datetime, date
from apps.social.models import (
    TipoActividad, EstadoActividad, ActividadComunitaria,
    AsistenciaActividad, ProgramaSocial, EstadoPrograma,
    TipoAutoridad, RolAutoridad, AutoridadComunitaria
)

pytestmark = pytest.mark.django_db

class TestSocialModels:
    def test_tipo_actividad_creation(self):
        tipo = TipoActividad.objects.create(
            nombre='Taller',
            descripcion='Actividad de taller'
        )
        assert tipo.nombre == 'Taller'
        assert str(tipo) == 'Taller'

    def test_estado_actividad_creation(self):
        estado = EstadoActividad.objects.create(
            nombre='Planificada',
            descripcion='Actividad planificada',
            color='#007bff'
        )
        assert estado.nombre == 'Planificada'
        assert str(estado) == 'Planificada'

    def test_actividad_comunitaria_creation(self, tipo_actividad, estado_actividad):
        actividad = ActividadComunitaria.objects.create(
            titulo='Taller de Computación',
            descripcion='Aprender computación básica',
            tipo_actividad=tipo_actividad,
            estado=estado_actividad,
            fecha_inicio=datetime(2024, 12, 15, 10, 0),
            ubicacion='Centro Comunitario',
            capacidad_maxima=20
        )
        assert actividad.titulo == 'Taller de Computación'
        assert actividad.tasa_participacion == 0
        assert actividad.asistentes_pendientes == 0
        expected_str = "Taller de Computación - 15/12/2024 10:00"
        assert str(actividad) == expected_str

    def test_actividad_comunitaria_with_asistentes(self, actividad_comunitaria, persona):
        actividad_comunitaria.asistentes_registrados.add(persona)
        actividad_comunitaria.asistentes_confirmados = 1
        actividad_comunitaria.save()

        assert actividad_comunitaria.asistentes_pendientes == 0
        assert actividad_comunitaria.tasa_participacion == 5.0  # 1/20 * 100

    def test_asistencia_actividad_creation(self, actividad_comunitaria, persona):
        asistencia = AsistenciaActividad.objects.create(
            actividad=actividad_comunitaria,
            persona=persona,
            confirmado=True
        )
        assert asistencia.confirmado == True
        assert str(asistencia) == f"{persona.nombre_completo} - {actividad_comunitaria.titulo}"

    def test_programa_social_creation(self, estado_programa, admin_user):
        programa = ProgramaSocial.objects.create(
            nombre='Programa Educativo',
            descripcion='Programa para educación comunitaria',
            tipo_programa='educacion',
            estado=estado_programa,
            responsable=admin_user
        )
        assert programa.nombre == 'Programa Educativo'
        assert programa.tipo_programa == 'educacion'
        assert str(programa) == 'Programa Educativo'

    def test_tipo_autoridad_creation(self):
        tipo = TipoAutoridad.objects.create(
            nombre='Comunitaria',
            descripcion='Autoridad comunitaria tradicional'
        )
        assert tipo.nombre == 'Comunitaria'
        assert str(tipo) == 'Comunitaria'

    def test_rol_autoridad_creation(self):
        rol = RolAutoridad.objects.create(
            nombre='Líder',
            descripcion='Líder comunitario'
        )
        assert rol.nombre == 'Líder'
        assert str(rol) == 'Líder'

    def test_autoridad_comunitaria_creation(self, persona, tipo_actividad, estado_actividad):
        # Crear tipo autoridad y rol primero
        tipo_autoridad = TipoAutoridad.objects.create(nombre='Comunitaria')
        rol_autoridad = RolAutoridad.objects.create(nombre='Líder')

        autoridad = AutoridadComunitaria.objects.create(
            persona=persona,
            tipo_autoridad=tipo_autoridad,
            rol=rol_autoridad,
            fecha_inicio_mandato=date(2024, 1, 1),
            telefono_contacto='123456789',
            activo=True
        )
        expected_str = f"{persona} - {rol_autoridad} ({tipo_autoridad})"
        assert str(autoridad) == expected_str
        assert autoridad.activo == True


class TestSocialViews:
    def test_tipo_actividad_list(self, api_client, admin_user, tipo_actividad):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:tipo_actividad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_estado_actividad_list(self, api_client, admin_user, estado_actividad):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:estado_actividad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_actividad_comunitaria_list(self, api_client, admin_user, actividad_comunitaria):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:actividad_comunitaria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_actividad_comunitaria_create(self, api_client, admin_user, tipo_actividad, estado_actividad):
        api_client.force_authenticate(user=admin_user)
        data = {
            'titulo': 'Nueva Actividad',
            'descripcion': 'Descripción de la actividad',
            'tipo_actividad_id': tipo_actividad.id,
            'estado_id': estado_actividad.id,
            'fecha_inicio': '2024-12-20T14:00:00Z',
            'ubicacion': 'Centro Comunitario',
            'capacidad_maxima': 30
        }
        url = reverse('social:actividad_comunitaria-list')
        response = api_client.post(url, data, format='json')
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['titulo'] == 'Nueva Actividad'

    def test_registrar_asistencia(self, api_client, admin_user, actividad_comunitaria, persona):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:actividad_comunitaria-registrar-asistencia', kwargs={'pk': actividad_comunitaria.pk})
        data = {
            'persona_id': persona.id,
            'confirmado': True,
            'observaciones': 'Asistencia confirmada'
        }
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['confirmado'] == True

        # Verificar que se actualizó el contador
        actividad_comunitaria.refresh_from_db()
        assert actividad_comunitaria.asistentes_confirmados == 1

    def test_actividad_estadisticas(self, api_client, admin_user, actividad_comunitaria, persona):
        # Agregar asistente
        actividad_comunitaria.asistentes_registrados.add(persona)
        actividad_comunitaria.asistentes_confirmados = 1
        actividad_comunitaria.save()

        api_client.force_authenticate(user=admin_user)
        url = reverse('social:actividad_comunitaria-estadisticas', kwargs={'pk': actividad_comunitaria.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_registrados'] == 1
        assert response.data['total_confirmados'] == 1
        assert response.data['tasa_participacion'] == 5.0

    def test_calendario_actividades(self, api_client, admin_user, actividad_comunitaria):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:actividad_comunitaria-calendario')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_asistencia_por_actividad(self, api_client, admin_user, asistencia_actividad):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:asistencia_actividad-por-actividad')
        data = {'actividad_id': asistencia_actividad.actividad.id}
        response = api_client.get(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_programa_social_list(self, api_client, admin_user, programa_social):
        api_client.force_authenticate(user=admin_user)
        url = reverse('social:programa-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_autoridad_comunitaria_list(self, api_client, admin_user, persona):
        # Crear autoridad primero
        tipo_autoridad = TipoAutoridad.objects.create(nombre='Comunitaria')
        rol_autoridad = RolAutoridad.objects.create(nombre='Líder')
        AutoridadComunitaria.objects.create(
            persona=persona,
            tipo_autoridad=tipo_autoridad,
            rol=rol_autoridad,
            fecha_inicio_mandato=date(2024, 1, 1)
        )

        api_client.force_authenticate(user=admin_user)
        url = reverse('social:autoridad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_unauthenticated_access(self, api_client):
        url = reverse('social:tipo_actividad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_access(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('social:tipo_actividad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
