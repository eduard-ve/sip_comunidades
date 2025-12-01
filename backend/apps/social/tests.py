import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from apps.social.models import (
    TipoAutoridad, RolAutoridad, AutoridadComunitaria,
    ProgramaSocial, EstadoPrograma, ActividadComunitaria, TipoActividad, EstadoActividad
)

pytestmark = pytest.mark.django_db

class TestTipoAutoridadModel:
    def test_tipo_autoridad_creation(self):
        tipo = TipoAutoridad.objects.create(
            nombre='Comunitario',
            descripcion='Líder comunitario'
        )
        assert tipo.nombre == 'Comunitario'
        assert tipo.descripcion == 'Líder comunitario'

    def test_tipo_autoridad_str(self):
        tipo = TipoAutoridad.objects.create(nombre='Tradicional')
        assert str(tipo) == 'Tradicional'


class TestRolAutoridadModel:
    def test_rol_autoridad_creation(self):
        rol = RolAutoridad.objects.create(
            nombre='Presidente',
            descripcion='Jefe de la comunidad'
        )
        assert rol.nombre == 'Presidente'

    def test_rol_autoridad_str(self):
        rol = RolAutoridad.objects.create(nombre='Secretario')
        assert str(rol) == 'Secretario'


class TestAutoridadComunitariaModel:
    def test_autoridad_comunitaria_creation(self, persona, tipo_identificacion, nivel_educativo, ocupacion, grupo_etnico, estado_civil, lengua):
        tipo_autoridad = TipoAutoridad.objects.create(nombre='Comunitario')
        rol = RolAutoridad.objects.create(nombre='Líder')
        autoridad = AutoridadComunitaria.objects.create(
            persona=persona,
            tipo_autoridad=tipo_autoridad,
            rol=rol,
            fecha_inicio_mandato=date.today()
        )
        assert autoridad.persona == persona
        assert autoridad.activo is True

    def test_autoridad_comunitaria_str(self, persona):
        tipo_autoridad = TipoAutoridad.objects.create(nombre='Comunitario')
        rol = RolAutoridad.objects.create(nombre='Líder')
        autoridad = AutoridadComunitaria.objects.create(
            persona=persona,
            tipo_autoridad=tipo_autoridad,
            rol=rol,
            fecha_inicio_mandato=date.today()
        )
        expected = f"{persona} - {rol} ({tipo_autoridad})"
        assert str(autoridad) == expected


class TestProgramaSocialModel:
    def test_programa_social_creation(self):
        estado = EstadoPrograma.objects.create(nombre='Activo')
        programa = ProgramaSocial.objects.create(
            nombre='Programa Educativo',
            descripcion='Apoyo educativo',
            tipo_programa='educacion',
            estado=estado
        )
        assert programa.nombre == 'Programa Educativo'
        assert programa.tipo_programa == 'educacion'
        assert programa.beneficiarios_count == 0

    def test_programa_social_str(self):
        estado = EstadoPrograma.objects.create(nombre='Activo')
        programa = ProgramaSocial.objects.create(
            nombre='Programa Salud',
            tipo_programa='salud',
            estado=estado
        )
        assert str(programa) == 'Programa Salud'


class TestActividadComunitariaModel:
    def test_actividad_comunitaria_creation(self):
        tipo_actividad = TipoActividad.objects.create(nombre='Taller')
        estado = EstadoActividad.objects.create(nombre='Planificada')
        from datetime import datetime
        actividad = ActividadComunitaria.objects.create(
            titulo='Taller de Computación',
            descripcion='Aprender computación',
            tipo_actividad=tipo_actividad,
            estado=estado,
            fecha_inicio=datetime.now(),
            capacidad_maxima=20
        )
        assert actividad.titulo == 'Taller de Computación'
        assert actividad.asistentes_confirmados == 0
        assert actividad.tasa_participacion == 0

    def test_actividad_comunitaria_str(self):
        tipo_actividad = TipoActividad.objects.create(nombre='Reunión')
        estado = EstadoActividad.objects.create(nombre='Completada')
        from datetime import datetime
        actividad = ActividadComunitaria.objects.create(
            titulo='Reunión Comunitaria',
            tipo_actividad=tipo_actividad,
            estado=estado,
            fecha_inicio=datetime.now()
        )
        expected = f"Reunión Comunitaria - {actividad.fecha_inicio.strftime('%d/%m/%Y %H:%M')}"
        assert str(actividad) == expected


class TestSocialViewSets:
    def test_tipo_autoridad_list_admin(self, api_client, admin_user):
        TipoAutoridad.objects.create(nombre='Test')
        api_client.force_authenticate(user=admin_user)
        url = reverse('tipoautoridad-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_programa_social_list_admin(self, api_client, admin_user):
        estado = EstadoPrograma.objects.create(nombre='Activo')
        ProgramaSocial.objects.create(
            nombre='Test Program',
            tipo_programa='educacion',
            estado=estado
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('programasocial-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_actividad_comunitaria_list_admin(self, api_client, admin_user):
        tipo_actividad = TipoActividad.objects.create(nombre='Test')
        estado = EstadoActividad.objects.create(nombre='Planificada')
        from datetime import datetime
        ActividadComunitaria.objects.create(
            titulo='Test Activity',
            tipo_actividad=tipo_actividad,
            estado=estado,
            fecha_inicio=datetime.now()
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('actividadcomunitaria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
