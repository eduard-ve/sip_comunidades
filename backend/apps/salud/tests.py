import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from apps.salud.models import (
    HistorialMedico, Vacuna, Medicamento, ExamenMedico,
    RegistroSalud, AlertaSalud, ControlSalud
)

pytestmark = pytest.mark.django_db

class TestSaludModels:
    def test_historial_medico_creation(self, persona):
        historial = HistorialMedico.objects.create(
            persona=persona,
            antecedentes_familiares='Diabetes',
            alergias='Penicilina',
            condiciones_cronicas='Hipertensión'
        )
        assert historial.persona == persona
        assert historial.antecedentes_familiares == 'Diabetes'
        expected_str = f"Historial médico de {persona}"
        assert str(historial) == expected_str

    def test_vacuna_creation(self, persona):
        vacuna = Vacuna.objects.create(
            persona=persona,
            nombre_vacuna='COVID-19',
            tipo_vacuna='campana',
            fecha_aplicacion=date(2024, 1, 15),
            dosis='Primera dosis'
        )
        assert vacuna.nombre_vacuna == 'COVID-19'
        assert vacuna.tipo_vacuna == 'campana'
        expected_str = f"COVID-19 - {persona} (2024-01-15)"
        assert str(vacuna) == expected_str

    def test_medicamento_creation(self, persona):
        medicamento = Medicamento.objects.create(
            persona=persona,
            nombre_medicamento='Paracetamol',
            dosis='500mg',
            frecuencia='Cada 8 horas',
            indicacion='Dolor de cabeza',
            fecha_prescripcion=date(2024, 1, 1),
            fecha_inicio=date(2024, 1, 1),
            activo=True
        )
        assert medicamento.nombre_medicamento == 'Paracetamol'
        assert medicamento.activo == True
        expected_str = f"Paracetamol - {persona}"
        assert str(medicamento) == expected_str

    def test_examen_medico_creation(self, persona):
        examen = ExamenMedico.objects.create(
            persona=persona,
            tipo_examen='laboratorio',
            nombre_examen='Hemograma',
            fecha_solicitud=date(2024, 1, 10),
            resultado='Normal'
        )
        assert examen.nombre_examen == 'Hemograma'
        assert examen.tipo_examen == 'laboratorio'
        expected_str = f"Hemograma - {persona} (2024-01-10)"
        assert str(examen) == expected_str

    def test_registro_salud_creation(self, persona):
        registro = RegistroSalud.objects.create(
            persona=persona,
            fecha_registro=date(2024, 1, 5),
            tipo_registro='Consulta',
            descripcion='Chequeo rutinario'
        )
        assert registro.tipo_registro == 'Consulta'
        expected_str = f"Registro de {persona} - Consulta (2024-01-05)"
        assert str(registro) == expected_str

    def test_alerta_salud_creation(self, persona):
        alerta = AlertaSalud.objects.create(
            persona=persona,
            titulo='Control mensual',
            descripcion='Requiere control de presión',
            prioridad='media'
        )
        assert alerta.titulo == 'Control mensual'
        assert alerta.prioridad == 'media'
        assert alerta.resuelta == False
        expected_str = f"Alerta para {persona} - Control mensual (media)"
        assert str(alerta) == expected_str

    def test_alerta_salud_sin_persona(self):
        alerta = AlertaSalud.objects.create(
            titulo='Alerta general',
            descripcion='Alerta sin persona específica',
            prioridad='alta'
        )
        expected_str = "Alerta para General - Alerta general (alta)"
        assert str(alerta) == expected_str

    def test_control_salud_creation(self, persona):
        control = ControlSalud.objects.create(
            persona=persona,
            tipo_control='Chequeo mensual',
            fecha_programada=date(2024, 2, 1)
        )
        assert control.tipo_control == 'Chequeo mensual'
        assert control.realizado == False
        expected_str = f"Control de {persona} - Chequeo mensual (2024-02-01)"
        assert str(control) == expected_str


class TestSaludViews:
    def test_registro_salud_list(self, api_client, admin_user, registro_salud):
        api_client.force_authenticate(user=admin_user)
        url = reverse('registros-salud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_alerta_salud_list(self, api_client, admin_user, alerta_salud):
        api_client.force_authenticate(user=admin_user)
        url = reverse('alertas-salud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_control_salud_list(self, api_client, admin_user, control_salud):
        api_client.force_authenticate(user=admin_user)
        url = reverse('controles-salud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_historial_medico_list(self, api_client, admin_user, historial_medico):
        api_client.force_authenticate(user=admin_user)
        url = reverse('historiales-medicos-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_vacuna_list(self, api_client, admin_user, vacuna):
        api_client.force_authenticate(user=admin_user)
        url = reverse('vacunas-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_medicamento_list(self, api_client, admin_user, medicamento):
        api_client.force_authenticate(user=admin_user)
        url = reverse('medicamentos-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_examen_medico_list(self, api_client, admin_user, examen_medico):
        api_client.force_authenticate(user=admin_user)
        url = reverse('examenes-medicos-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_registro_salud_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'fecha_registro': '2024-01-10',
            'tipo_registro': 'Consulta médica',
            'descripcion': 'Consulta de rutina'
        }
        url = reverse('registros-salud-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_alerta_salud_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'titulo': 'Nueva alerta',
            'descripcion': 'Descripción de la alerta',
            'prioridad': 'alta'
        }
        url = reverse('alertas-salud-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_control_salud_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'tipo_control': 'Vacunación',
            'fecha_programada': '2024-02-15'
        }
        url = reverse('controles-salud-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_vacuna_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'nombre_vacuna': 'Influenza',
            'tipo_vacuna': 'rutinaria',
            'fecha_aplicacion': '2024-01-20',
            'dosis': 'Única'
        }
        url = reverse('vacunas-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_medicamento_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'nombre_medicamento': 'Ibuprofeno',
            'dosis': '400mg',
            'frecuencia': 'Cada 6 horas',
            'indicacion': 'Dolor',
            'fecha_prescripcion': '2024-01-15',
            'fecha_inicio': '2024-01-15'
        }
        url = reverse('medicamentos-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_examen_medico_create(self, api_client, admin_user, persona):
        api_client.force_authenticate(user=admin_user)
        data = {
            'persona': persona.id,
            'tipo_examen': 'imagen',
            'nombre_examen': 'Radiografía de tórax',
            'fecha_solicitud': '2024-01-12'
        }
        url = reverse('examenes-medicos-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_salud_stats_kpis(self, api_client, registro_salud, alerta_salud, control_salud):
        url = reverse('salud-stats-kpis-salud')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'registros_salud' in response.data
        assert 'alertas_activas' in response.data
        assert response.data['registros_salud'] == 1
        assert response.data['alertas_activas'] == 1

    def test_enfermedades_comunes(self, api_client, registro_salud):
        url = reverse('salud-stats-enfermedades-comunes')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_distribucion_edad_salud(self, api_client, registro_salud):
        url = reverse('salud-stats-distribucion-edad-salud')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert isinstance(response.data, list)

    def test_unauthenticated_access(self, api_client):
        url = reverse('registros-salud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_access(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('registros-salud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
