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
from datetime import date, datetime

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

# Encuestas fixtures
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

# Poblacion fixtures
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

# Social fixtures
@pytest.fixture
def tipo_actividad():
    from apps.social.models import TipoActividad
    return TipoActividad.objects.create(
        nombre='Taller',
        descripcion='Actividad de taller comunitario'
    )

@pytest.fixture
def estado_actividad():
    from apps.social.models import EstadoActividad
    return EstadoActividad.objects.create(
        nombre='Planificada',
        descripcion='Actividad planificada'
    )

@pytest.fixture
def estado_programa():
    from apps.social.models import EstadoPrograma
    return EstadoPrograma.objects.create(nombre='Activo')

@pytest.fixture
def programa_social(estado_programa, admin_user):
    from apps.social.models import ProgramaSocial
    return ProgramaSocial.objects.create(
        nombre='Programa Educativo',
        descripcion='Programa para educación comunitaria',
        tipo_programa='educacion',
        estado=estado_programa,
        responsable=admin_user
    )

@pytest.fixture
def actividad_comunitaria(tipo_actividad, estado_actividad):
    from apps.social.models import ActividadComunitaria
    return ActividadComunitaria.objects.create(
        titulo='Taller de Computación',
        descripcion='Aprender computación básica',
        tipo_actividad=tipo_actividad,
        estado=estado_actividad,
        fecha_inicio=datetime(2024, 12, 15, 10, 0),
        ubicacion='Centro Comunitario',
        capacidad_maxima=20
    )

@pytest.fixture
def asistencia_actividad(actividad_comunitaria, persona):
    from apps.social.models import AsistenciaActividad
    return AsistenciaActividad.objects.create(
        actividad=actividad_comunitaria,
        persona=persona,
        confirmado=True
    )

# Salud fixtures
@pytest.fixture
def historial_medico(persona):
    from apps.salud.models import HistorialMedico
    return HistorialMedico.objects.create(
        persona=persona,
        antecedentes_familiares='Diabetes en la familia',
        alergias='Penicilina',
        condiciones_cronicas='Hipertensión'
    )

@pytest.fixture
def vacuna(persona):
    from apps.salud.models import Vacuna
    return Vacuna.objects.create(
        persona=persona,
        nombre_vacuna='COVID-19',
        tipo_vacuna='campana',
        fecha_aplicacion=date(2024, 1, 15),
        dosis='Primera dosis',
        lote='ABC123'
    )

@pytest.fixture
def medicamento(persona):
    from apps.salud.models import Medicamento
    return Medicamento.objects.create(
        persona=persona,
        nombre_medicamento='Paracetamol',
        dosis='500mg',
        frecuencia='Cada 8 horas',
        indicacion='Dolor de cabeza',
        fecha_prescripcion=date(2024, 1, 1),
        fecha_inicio=date(2024, 1, 1),
        activo=True
    )

@pytest.fixture
def examen_medico(persona):
    from apps.salud.models import ExamenMedico
    return ExamenMedico.objects.create(
        persona=persona,
        tipo_examen='laboratorio',
        nombre_examen='Hemograma completo',
        fecha_solicitud=date(2024, 1, 10),
        resultado='Normal'
    )

@pytest.fixture
def registro_salud(persona):
    from apps.salud.models import RegistroSalud
    return RegistroSalud.objects.create(
        persona=persona,
        fecha_registro=date(2024, 1, 5),
        tipo_registro='Consulta general',
        descripcion='Chequeo rutinario'
    )

@pytest.fixture
def alerta_salud(persona):
    from apps.salud.models import AlertaSalud
    return AlertaSalud.objects.create(
        persona=persona,
        titulo='Control de presión arterial',
        descripcion='Paciente con hipertensión requiere control mensual',
        prioridad='media'
    )

@pytest.fixture
def control_salud(persona):
    from apps.salud.models import ControlSalud
    return ControlSalud.objects.create(
        persona=persona,
        tipo_control='Chequeo mensual',
        fecha_programada=date(2024, 2, 1)
    )

# Reportes fixtures
@pytest.fixture
def reporte_salud(admin_user):
    from apps.reportes.models import ReporteSalud
    return ReporteSalud.objects.create(
        tipo_reporte='Resumen mensual',
        datos_agregados={
            'total_registros': 150,
            'total_alertas': 5,
            'alertas_activas': 3,
            'controles_pendientes': 12
        },
        fecha_reporte=date(2024, 12, 1),
        generado_por='admin'
    )

@pytest.fixture
def reporte_social(admin_user):
    from apps.reportes.models import ReporteSocial
    return ReporteSocial.objects.create(
        tipo_reporte='Programas sociales',
        datos_agregados={
            'total_programas': 25,
            'programas_activos': 20,
            'programas_egresados': 5
        },
        fecha_reporte=date(2024, 12, 1),
        generado_por='admin'
    )

@pytest.fixture
def reporte_encuestas(admin_user):
    from apps.reportes.models import ReporteEncuestas
    return ReporteEncuestas.objects.create(
        tipo_reporte='Resultados encuestas',
        datos_agregados={
            'total_respuestas_persona': 500,
            'estadisticas_generales': {
                'encuestas_activas': 5,
                'total_preguntas': 25
            }
        },
        fecha_reporte=date(2024, 12, 1),
        generado_por='admin'
    )