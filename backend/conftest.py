import os
import django
from django.conf import settings

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'sip.settings')
django.setup()

import pytest
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from apps.auditoria.models import AuditLog

User = get_user_model()

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user():
    return User.objects.create_user(
        username='testuser',
        email='test@example.com',
        password='testpass123',
        rol='user'
    )

@pytest.fixture
def admin_user():
    return User.objects.create_user(
        username='admin',
        email='admin@example.com',
        password='adminpass123',
        rol='admin'
    )

@pytest.fixture
def audit_log(user):
    return AuditLog.objects.create(
        usuario=user,
        accion='CREATE',
        modelo='TestModel',
        objeto_id='1',
        descripcion='Test audit log',
        ip_address='127.0.0.1',
        user_agent='Test Agent'
    )

@pytest.fixture
def encuesta():
    from apps.encuestas.models import Encuesta
    return Encuesta.objects.create(
        titulo='Test Survey',
        descripcion='A test survey',
        estado='activa'
    )

@pytest.fixture
def pregunta(encuesta):
    from apps.encuestas.models import Pregunta
    return Pregunta.objects.create(
        encuesta=encuesta,
        texto_pregunta='What is your favorite color?',
        tipo='opcion_multiple',
        orden=1
    )

@pytest.fixture
def opcion(pregunta):
    from apps.encuestas.models import Opcion
    return Opcion.objects.create(
        pregunta=pregunta,
        texto_opcion='Blue',
        valor=1
    )

@pytest.fixture
def respuesta(encuesta, pregunta, opcion):
    from apps.encuestas.models import Respuesta
    return Respuesta.objects.create(
        encuesta=encuesta,
        pregunta=pregunta,
        opcion=opcion,
        respuesta_texto='Blue is nice'
    )

@pytest.fixture
def tipo_identificacion():
    from apps.poblacion.models.catalogos import TipoIdentificacion
    return TipoIdentificacion.objects.create(nombre='Cédula')

@pytest.fixture
def nivel_educativo():
    from apps.poblacion.models.catalogos import NivelEducativo
    return NivelEducativo.objects.create(nombre='Secundaria')

@pytest.fixture
def ocupacion():
    from apps.poblacion.models.catalogos import Ocupacion
    return Ocupacion.objects.create(nombre='Ingeniero')

@pytest.fixture
def grupo_etnico():
    from apps.poblacion.models.catalogos import GrupoEtnico
    return GrupoEtnico.objects.create(nombre='Indígena')

@pytest.fixture
def estado_civil():
    from apps.poblacion.models.catalogos import EstadoCivil
    return EstadoCivil.objects.create(nombre='Soltero')

@pytest.fixture
def lengua():
    from apps.poblacion.models.catalogos import Lengua
    return Lengua.objects.create(nombre='Español')

@pytest.fixture
def tipo_relacion():
    from apps.poblacion.models.catalogos import TipoRelacion
    return TipoRelacion.objects.create(nombre='Padre')

@pytest.fixture
def persona(tipo_identificacion, nivel_educativo, ocupacion, grupo_etnico, estado_civil, lengua):
    from apps.poblacion.models.personas import Persona
    from datetime import date
    return Persona.objects.create(
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

@pytest.fixture
def persona2(tipo_identificacion, nivel_educativo, ocupacion, grupo_etnico, estado_civil, lengua):
    from apps.poblacion.models.personas import Persona
    from datetime import date
    return Persona.objects.create(
        tipo_identificacion=tipo_identificacion,
        numero_identificacion='87654321',
        primer_nombre='María',
        primer_apellido='García',
        fecha_nacimiento=date(1992, 5, 15),
        genero='F',
        nivel_educativo=nivel_educativo,
        ocupacion=ocupacion,
        grupo_etnico=grupo_etnico,
        estado_civil=estado_civil,
        lengua_materna=lengua
    )

@pytest.fixture
def relacion_familiar(persona, persona2, tipo_relacion):
    from apps.poblacion.models.relaciones import RelacionFamiliar
    return RelacionFamiliar.objects.create(
        persona=persona,
        familiar=persona2,
        tipo_relacion=tipo_relacion
    )