import pytest
from django.urls import reverse
from rest_framework import status
from datetime import date
from apps.reportes.models import ReporteSalud, ReporteSocial, ReporteEncuestas

pytestmark = pytest.mark.django_db

class TestReporteSaludModel:
    def test_reporte_salud_creation(self):
        reporte = ReporteSalud.objects.create(
            tipo_reporte='Resumen Salud',
            datos_agregados={'total_registros': 100},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        assert reporte.tipo_reporte == 'Resumen Salud'
        assert reporte.datos_agregados == {'total_registros': 100}
        assert reporte.generado_por == 'admin'

    def test_reporte_salud_str(self):
        reporte = ReporteSalud.objects.create(
            tipo_reporte='Indicadores',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='user'
        )
        expected = f"Reporte Salud - Indicadores ({date.today()}) - user"
        assert str(reporte) == expected

    def test_reporte_salud_unique_together(self):
        ReporteSalud.objects.create(
            tipo_reporte='Test',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='user'
        )
        with pytest.raises(Exception):  # IntegrityError
            ReporteSalud.objects.create(
                tipo_reporte='Test',
                datos_agregados={},
                fecha_reporte=date.today(),
                generado_por='user'
            )


class TestReporteSocialModel:
    def test_reporte_social_creation(self):
        reporte = ReporteSocial.objects.create(
            tipo_reporte='Apoyo Social',
            datos_agregados={'total_programas': 50},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        assert reporte.tipo_reporte == 'Apoyo Social'
        assert reporte.datos_agregados == {'total_programas': 50}

    def test_reporte_social_str(self):
        reporte = ReporteSocial.objects.create(
            tipo_reporte='Condiciones',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='user'
        )
        expected = f"Reporte Social - Condiciones ({date.today()}) - user"
        assert str(reporte) == expected


class TestReporteEncuestasModel:
    def test_reporte_encuestas_creation(self):
        reporte = ReporteEncuestas.objects.create(
            tipo_reporte='Resultados',
            datos_agregados={'total_respuestas': 200},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        assert reporte.tipo_reporte == 'Resultados'
        assert reporte.datos_agregados == {'total_respuestas': 200}

    def test_reporte_encuestas_str(self):
        reporte = ReporteEncuestas.objects.create(
            tipo_reporte='Análisis',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='user'
        )
        expected = f"Reporte Encuestas - Análisis ({date.today()}) - user"
        assert str(reporte) == expected


class TestReporteSaludViewSet:
    def test_list_reportes_salud_admin(self, api_client, admin_user):
        reporte = ReporteSalud.objects.create(
            tipo_reporte='Test',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('reportesalud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1

    def test_create_reporte_salud_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'tipo_reporte': 'Nuevo Reporte',
            'datos_agregados': {'test': 'data'},
            'fecha_reporte': date.today().isoformat(),
            'generado_por': 'admin'
        }
        url = reverse('reportesalud-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED

    def test_unauthenticated_access(self, api_client):
        url = reverse('reportesalud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_access(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('reportesalud-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN


class TestReporteSocialViewSet:
    def test_list_reportes_social_admin(self, api_client, admin_user):
        reporte = ReporteSocial.objects.create(
            tipo_reporte='Test',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('reportesocial-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1


class TestReporteEncuestasViewSet:
    def test_list_reportes_encuestas_admin(self, api_client, admin_user):
        reporte = ReporteEncuestas.objects.create(
            tipo_reporte='Test',
            datos_agregados={},
            fecha_reporte=date.today(),
            generado_por='admin'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('reporteencuestas-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
