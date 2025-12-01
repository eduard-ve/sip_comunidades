import pytest
from django.urls import reverse
from rest_framework import status
from apps.poblacion.models.personas import Persona
from apps.poblacion.models.catalogos import TipoIdentificacion, NivelEducativo, Ocupacion
from apps.poblacion.models.relaciones import RelacionFamiliar

pytestmark = pytest.mark.django_db

class TestCatalogoBase:
    def test_catalogo_str(self):
        tipo_id = TipoIdentificacion.objects.create(nombre='Cédula')
        assert str(tipo_id) == 'Cédula'

    def test_catalogo_unique_name(self):
        TipoIdentificacion.objects.create(nombre='Cédula')
        with pytest.raises(Exception):  # IntegrityError
            TipoIdentificacion.objects.create(nombre='Cédula')

    def test_catalogo_ordering(self):
        tipo2 = TipoIdentificacion.objects.create(nombre='B - Second')
        tipo1 = TipoIdentificacion.objects.create(nombre='A - First')
        tipos = list(TipoIdentificacion.objects.all())
        assert tipos[0] == tipo1
        assert tipos[1] == tipo2


class TestPersonaModel:
    def test_persona_creation(self, tipo_identificacion, nivel_educativo, ocupacion, grupo_etnico, estado_civil, lengua):
        from datetime import date
        persona = Persona.objects.create(
            tipo_identificacion=tipo_identificacion,
            numero_identificacion='12345678',
            primer_nombre='Juan',
            primer_apellido='Pérez',
            fecha_nacimiento=date(1990, 1, 1),
            genero='M',
            nivel_educativo=nivel_educativo,
            ocupacion=ocupacion,
            grupo_etnico=grupo_etnico,
            estado_civil=estado_civil,
            lengua_materna=lengua
        )
        assert persona.nombre_completo == 'Juan Pérez'
        assert persona.genero == 'M'

    def test_persona_str(self, persona):
        expected = f"{persona.nombre_completo} - {persona.numero_identificacion}"
        assert str(persona) == expected

    def test_persona_genero_choices(self):
        choices = dict(Persona.GENERO_CHOICES)
        assert 'M' in choices
        assert 'F' in choices
        assert 'O' in choices

    def test_persona_ordering(self, persona, persona2):
        personas = list(Persona.objects.all())
        # Should be ordered by primer_apellido, primer_nombre
        assert personas[0].primer_apellido <= personas[1].primer_apellido


class TestRelacionFamiliarModel:
    def test_relacion_familiar_creation(self, persona, persona2, tipo_relacion):
        relacion = RelacionFamiliar.objects.create(
            persona=persona,
            familiar=persona2,
            tipo_relacion=tipo_relacion
        )
        assert relacion.persona == persona
        assert relacion.familiar == persona2
        assert relacion.tipo_relacion == tipo_relacion

    def test_relacion_familiar_str(self, relacion_familiar):
        expected = f"{relacion_familiar.persona} - {relacion_familiar.tipo_relacion} - {relacion_familiar.familiar}"
        assert str(relacion_familiar) == expected

    def test_no_auto_relacion(self, persona, tipo_relacion):
        # Should not allow self-relation
        with pytest.raises(Exception):  # IntegrityError from constraint
            RelacionFamiliar.objects.create(
                persona=persona,
                familiar=persona,
                tipo_relacion=tipo_relacion
            )


class TestPersonaViewSet:
    def test_list_personas_admin(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        url = reverse('persona-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 1

    def test_create_persona_admin(self, api_client, admin_user, tipo_identificacion, nivel_educativo, ocupacion, grupo_etnico, estado_civil, lengua):
        api_client.force_authenticate(user=admin_user)
        data = {
            'tipo_identificacion': tipo_identificacion.id,
            'numero_identificacion': '99999999',
            'primer_nombre': 'Test',
            'primer_apellido': 'User',
            'fecha_nacimiento': '1990-01-01',
            'genero': 'M',
            'nivel_educativo': nivel_educativo.id,
            'ocupacion': ocupacion.id,
            'grupo_etnico': grupo_etnico.id,
            'estado_civil': estado_civil.id,
            'lengua_materna': lengua.id
        }
        url = reverse('persona-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthenticated_access(self, api_client):
        url = reverse('persona-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_access(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('persona-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestEstadisticasViewSet:
    def test_estadisticas_endpoint(self, api_client, persona):
        url = reverse('estadisticas-estadisticas')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'poblacion_total' in response.data
        assert 'edad_promedio' in response.data

    def test_distribucion_edad(self, api_client, persona):
        url = reverse('estadisticas-distribucion-edad')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_top_ocupaciones(self, api_client, persona):
        url = reverse('estadisticas-top-ocupaciones')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_dashboard(self, api_client, persona):
        url = reverse('estadisticas-dashboard')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'hero_metrics' in response.data
        assert 'gestion_social' in response.data

    def test_personas_filtradas(self, api_client, persona):
        url = reverse('estadisticas-personas-filtradas')
        response = api_client.get(url, {'genero': 'M'})
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_relaciones_familiares(self, api_client, persona):
        url = reverse('estadisticas-relaciones-familiares', kwargs={'pk': persona.id})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)
