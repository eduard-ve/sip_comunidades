from django.test import TestCase

import pytest
from rest_framework.test import APIClient
from django.urls import reverse
from apps.poblacion.models import (
    Persona,
    TipoIdentificacion,
    NivelEducativo,
    Ocupacion,
    GrupoFamiliar,
    EstadoCivil,
    Lengua,
)
from apps.usuarios.models import Usuario


@pytest.fixture
def api_client():
    return APIClient()


@pytest.fixture
def usuario_admin(db):
    """Crea un usuario admin para autenticación"""
    user = Usuario.objects.create_user(
        username="admin_test",
        email="admin@test.com",
        password="123456",
        rol="admin",
        is_staff=True,
    )
    return user


@pytest.fixture
def autenticado(api_client, usuario_admin):
    """Autentica al usuario admin y devuelve el cliente autenticado"""
    api_client.force_authenticate(user=usuario_admin)
    return api_client


@pytest.fixture
def datos_base(db):
    """Crea registros base de catálogos poblacionales"""
    tipo_id = TipoIdentificacion.objects.create(nombre="Cédula")
    nivel = NivelEducativo.objects.create(nombre="Secundaria")
    ocupacion = Ocupacion.objects.create(nombre="Agricultor")
    grupo = GrupoFamiliar.objects.create(nombre="Familia Pérez")
    estado_civil = EstadoCivil.objects.create(nombre="Soltero")
    lengua = Lengua.objects.create(nombre="Español")

    return {
        "tipo_identificacion": tipo_id,
        "nivel_educativo": nivel,
        "ocupacion": ocupacion,
        "grupo_familiar": grupo,
        "estado_civil": estado_civil,
        "lengua": lengua,
    }


@pytest.mark.django_db
def test_crear_persona(autenticado, datos_base):
    """Debe crear una persona correctamente vía API"""
    url = reverse("personas-list")
    payload = {
        "tipo_identificacion": datos_base["tipo_identificacion"].id,
        "numero_identificacion": "1234567890",
        "primer_nombre": "Juan",
        "segundo_nombre": "Carlos",
        "primer_apellido": "Pérez",
        "segundo_apellido": "Gómez",
        "fecha_nacimiento": "1990-01-01",
        "genero": "M",
        "direccion": "Calle 123",
        "nivel_educativo": datos_base["nivel_educativo"].id,
        "ocupacion": datos_base["ocupacion"].id,
        "grupo_familiar": datos_base["grupo_familiar"].id,
        "estado_civil": datos_base["estado_civil"].id,
        "lengua_materna": datos_base["lengua"].id,
    }

    response = autenticado.post(url, payload, format="json")

    assert response.status_code == 201, response.data
    assert Persona.objects.filter(numero_identificacion="1234567890").exists()


@pytest.mark.django_db
def test_listar_personas(autenticado, datos_base):
    """Debe listar personas correctamente"""
    persona = Persona.objects.create(
        tipo_identificacion=datos_base["tipo_identificacion"],
        numero_identificacion="987654321",
        primer_nombre="María",
        primer_apellido="López",
        fecha_nacimiento="1985-02-10",
        genero="F",
    )

    url = reverse("personas-list")
    response = autenticado.get(url)
    assert response.status_code == 200
    assert any(p["numero_identificacion"] == persona.numero_identificacion for p in response.data)


@pytest.mark.django_db
def test_detalle_persona(autenticado, datos_base):
    """Debe obtener el detalle de una persona"""
    persona = Persona.objects.create(
        tipo_identificacion=datos_base["tipo_identificacion"],
        numero_identificacion="55555",
        primer_nombre="Carlos",
        primer_apellido="Ruiz",
        fecha_nacimiento="1999-05-10",
        genero="M",
    )
    url = reverse("personas-detail", args=[persona.id])
    response = autenticado.get(url)
    assert response.status_code == 200
    assert response.data["primer_nombre"] == "Carlos"


@pytest.mark.django_db
def test_actualizar_persona(autenticado, datos_base):
    """Debe actualizar correctamente los datos de una persona"""
    persona = Persona.objects.create(
        tipo_identificacion=datos_base["tipo_identificacion"],
        numero_identificacion="99999",
        primer_nombre="Ana",
        primer_apellido="García",
        fecha_nacimiento="2000-07-10",
        genero="F",
    )

    url = reverse("personas-detail", args=[persona.id])
    payload = {"primer_nombre": "Ana María"}
    response = autenticado.patch(url, payload, format="json")

    assert response.status_code == 200
    persona.refresh_from_db()
    assert persona.primer_nombre == "Ana María"


@pytest.mark.django_db
def test_eliminar_persona(autenticado, datos_base):
    """Debe eliminar una persona correctamente"""
    persona = Persona.objects.create(
        tipo_identificacion=datos_base["tipo_identificacion"],
        numero_identificacion="88888",
        primer_nombre="Pedro",
        primer_apellido="Rojas",
        fecha_nacimiento="1991-08-01",
        genero="M",
    )

    url = reverse("personas-detail", args=[persona.id])
    response = autenticado.delete(url)
    assert response.status_code in [204, 200]
    assert not Persona.objects.filter(id=persona.id).exists()

