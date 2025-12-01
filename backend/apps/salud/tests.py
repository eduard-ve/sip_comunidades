import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from apps.salud.models import HistorialMedico, Vacuna, Medicamento, RegistroSalud, AlertaSalud, ControlSalud

pytestmark = pytest.mark.django_db

class TestHistorialMedicoModel:
    def test_historial_medico_creation(self, persona):
        historial = HistorialMedico.objects.create(
            persona=persona,
            antecedentes_familiares='Diabetes',
            alergias='Penicilina'
        )
        assert historial.persona == persona
        assert historial.antecedentes_familiares == 'Diabetes'
        assert historial.alergias == 'Penicilina'

    def test_historial_medico_str(self, persona):
        historial = HistorialMedico.objects.create(persona=persona)
        expected = f"Historial médico de {persona}"
        assert str(historial) == expected


class TestVacunaModel:
    def test_vacuna_creation(self, persona):
        vacuna = Vacuna.objects.create(
            persona=persona,
            nombre_vacuna='COVID-19',
            tipo_vacuna='campana',
            fecha_aplicacion=date.today(),
            dosis='1ra dosis'
        )
        assert vacuna.persona == persona
        assert vacuna.nombre_vacuna == 'COVID-19'
        assert vacuna.tipo_vacuna == 'campana'

    def test_vacuna_str(self, persona):
        vacuna = Vacuna.objects.create(
            persona=persona,
            nombre_vacuna='Sarampión',
            fecha_aplicacion=date.today()
        )
        expected = f"Sarampión - {persona} ({date.today()})"
        assert str(vacuna) == expected


class TestMedicamentoModel:
    def test_medicamento_creation(self, persona):
        medicamento = Medicamento.objects.create(
            persona=persona,
            nombre_medicamento='Paracetamol',
            dosis='500mg',
            frecuencia='Cada 8 horas',
            indicacion='Dolor de cabeza',
            fecha_prescripcion=date.today(),
            fecha_inicio=date.today()
        )
        assert medicamento.persona == persona
        assert medicamento.nombre_medicamento == 'Paracetamol'
        assert medicamento.activo is True

    def test_medicamento_str(self, persona):
        medicamento = Medicamento.objects.create(
            persona=persona,
            nombre_medicamento='Ibuprofeno',
            dosis='200mg',
            frecuencia='Cada 6 horas',
            indicacion='Inflamación',
            fecha_prescripcion=date.today(),
            fecha_inicio=date.today()
        )
        expected = f"Ibuprofeno - {persona}"
        assert str(medicamento) == expected


class TestRegistroSaludModel:
    def test_registro_salud_creation(self, persona):
        registro = RegistroSalud.objects.create(
            persona=persona,
            fecha_registro=date.today(),
            tipo_registro='Consulta',
            descripcion='Chequeo general'
        )
        assert registro.persona == persona
        assert registro.tipo_registro == 'Consulta'
        assert registro.descripcion == 'Chequeo general'

    def test_registro_salud_str(self, persona):
        registro = RegistroSalud.objects.create(
            persona=persona,
            fecha_registro=date.today(),
            tipo_registro='Vacunación'
        )
        expected = f"Registro de {persona} - Vacunación ({date.today()})"
        assert str(registro) == expected


class TestAlertaSaludModel:
    def test_alerta_salud_creation(self, persona):
        alerta = AlertaSalud.objects.create(
            persona=persona,
            titulo='Presión alta',
            descripcion='Paciente con hipertensión',
            prioridad='alta'
        )
        assert alerta.persona == persona
        assert alerta.titulo == 'Presión alta'
        assert alerta.prioridad == 'alta'
        assert alerta.resuelta is False

    def test_alerta_salud_str(self, persona):
        alerta = AlertaSalud.objects.create(
            persona=persona,
            titulo='Fiebre',
            descripcion='Temperatura elevada',
            prioridad='media'
        )
        expected = f"Alerta para {persona} - Fiebre (media)"
        assert str(alerta) == expected

    def test_alerta_salud_str_general(self):
        alerta = AlertaSalud.objects.create(
            titulo='Alerta general',
            descripcion='Alerta sin persona específica',
            prioridad='baja'
        )
        expected = "Alerta para General - Alerta general (baja)"
        assert str(alerta) == expected


class TestControlSaludModel:
    def test_control_salud_creation(self, persona):
        control = ControlSalud.objects.create(
            persona=persona,
            tipo_control='Chequeo anual',
            fecha_programada=date.today()
        )
        assert control.persona == persona
        assert control.tipo_control == 'Chequeo anual'
        assert control.realizado is False

    def test_control_salud_str(self, persona):
        control = ControlSalud.objects.create(
            persona=persona,
            tipo_control='Vacunación',
            fecha_programada=date.today()
        )
        expected = f"Control de {persona} - Vacunación ({date.today()})"
        assert str(control) == expected


class TestSaludViewSets:
    def test_historial_medico_list_admin(self, api_client, admin_user, persona):
        HistorialMedico.objects.create(persona=persona)
        api_client.force_authenticate(user=admin_user)
        url = reverse('historialmedico-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_vacuna_list_admin(self, api_client, admin_user, persona):
        Vacuna.objects.create(
            persona=persona,
            nombre_vacuna='Test',
            fecha_aplicacion=date.today()
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('vacuna-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK

    def test_medicamento_list_admin(self, api_client, admin_user, persona):
        Medicamento.objects.create(
            persona=persona,
            nombre_medicamento='Test',
            dosis='100mg',
            frecuencia='Diario',
            indicacion='Test',
            fecha_prescripcion=date.today(),
            fecha_inicio=date.today()
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('medicamento-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
