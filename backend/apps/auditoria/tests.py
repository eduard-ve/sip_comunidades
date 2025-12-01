import pytest
from django.urls import reverse
from rest_framework import status
from apps.auditoria.models import AuditLog

pytestmark = pytest.mark.django_db

class TestAuditLogModel:
    def test_audit_log_creation(self, user):
        audit = AuditLog.objects.create(
            usuario=user,
            accion='CREATE',
            modelo='TestModel',
            objeto_id='1',
            descripcion='Test creation',
            ip_address='192.168.1.1',
            user_agent='Mozilla/5.0'
        )
        assert audit.usuario == user
        assert audit.accion == 'CREATE'
        assert audit.modelo == 'TestModel'
        assert audit.objeto_id == '1'
        assert audit.descripcion == 'Test creation'
        assert audit.ip_address == '192.168.1.1'
        assert audit.user_agent == 'Mozilla/5.0'
        assert audit.datos_anteriores is None
        assert audit.datos_nuevos is None

    def test_audit_log_str(self, user):
        audit = AuditLog.objects.create(
            usuario=user,
            accion='UPDATE',
            modelo='User',
            objeto_id=str(user.id),
            descripcion='Updated user'
        )
        expected = f"{user} - UPDATE - User - {audit.fecha}"
        assert str(audit) == expected

    def test_audit_log_choices(self):
        choices = dict(AuditLog.ACTION_CHOICES)
        assert 'CREATE' in choices
        assert 'UPDATE' in choices
        assert 'DELETE' in choices
        assert 'LOGIN' in choices
        assert 'LOGOUT' in choices
        assert 'VIEW' in choices

    def test_audit_log_ordering(self, user):
        # Create multiple logs
        audit1 = AuditLog.objects.create(
            usuario=user, accion='CREATE', modelo='Model1', descripcion='First'
        )
        audit2 = AuditLog.objects.create(
            usuario=user, accion='UPDATE', modelo='Model2', descripcion='Second'
        )
        # Should be ordered by -fecha, so audit2 first
        logs = list(AuditLog.objects.all())
        assert logs[0] == audit2
        assert logs[1] == audit1


class TestAuditLogSerializer:
    def test_serializer_fields(self, audit_log):
        from apps.auditoria.serializers import AuditLogSerializer
        serializer = AuditLogSerializer(audit_log)
        data = serializer.data
        assert 'id_audit' in data
        assert 'usuario' in data
        assert 'usuario_username' in data
        assert 'usuario_rol' in data
        assert 'accion' in data
        assert 'modelo' in data
        assert 'objeto_id' in data
        assert 'descripcion' in data
        assert 'ip_address' in data
        assert 'fecha' in data
        assert 'datos_anteriores' in data
        assert 'datos_nuevos' in data

    def test_serializer_read_only_fields(self, audit_log):
        from apps.auditoria.serializers import AuditLogSerializer
        serializer = AuditLogSerializer(audit_log)
        assert serializer.fields['id_audit'].read_only
        assert serializer.fields['fecha'].read_only

    def test_serializer_with_null_user(self):
        audit = AuditLog.objects.create(
            usuario=None,
            accion='LOGIN',
            modelo='User',
            descripcion='Anonymous login'
        )
        from apps.auditoria.serializers import AuditLogSerializer
        serializer = AuditLogSerializer(audit)
        data = serializer.data
        assert data['usuario'] is None
        assert data['usuario_username'] == ''
        assert data['usuario_rol'] == ''


class TestAuditLogViewSet:
    def test_list_audit_logs_admin(self, api_client, admin_user, audit_log):
        api_client.force_authenticate(user=admin_user)
        url = reverse('auditoria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 1
        assert response.data[0]['id_audit'] == audit_log.id_audit

    def test_list_audit_logs_user(self, api_client, user, admin_user, audit_log):
        # Create another log for different user (admin)
        AuditLog.objects.create(
            usuario=admin_user,
            accion='DELETE',
            modelo='Test',
            descripcion='Admin action'
        )
        api_client.force_authenticate(user=user)
        url = reverse('auditoria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        # Should only see their own logs
        assert len(response.data) == 1
        assert response.data[0]['usuario'] == user.id

    def test_retrieve_audit_log(self, api_client, admin_user, audit_log):
        api_client.force_authenticate(user=admin_user)
        url = reverse('auditoria-detail', kwargs={'pk': audit_log.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['id_audit'] == audit_log.id_audit

    def test_unauthenticated_access(self, api_client):
        url = reverse('auditoria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_ordering(self, api_client, admin_user, user):
        # Create logs with different dates
        audit1 = AuditLog.objects.create(
            usuario=user, accion='CREATE', modelo='Model1', descripcion='First'
        )
        audit2 = AuditLog.objects.create(
            usuario=user, accion='UPDATE', modelo='Model2', descripcion='Second'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('auditoria-list')
        response = api_client.get(url, {'ordering': 'fecha'})
        assert response.status_code == status.HTTP_200_OK
        # Should be ordered by fecha ascending
        assert response.data[0]['id_audit'] == audit1.id_audit
        assert response.data[1]['id_audit'] == audit2.id_audit

    def test_stats_action_admin(self, api_client, admin_user, audit_log):
        # Create more logs for stats
        AuditLog.objects.create(
            usuario=admin_user, accion='UPDATE', modelo='User', descripcion='Update'
        )
        AuditLog.objects.create(
            usuario=admin_user, accion='DELETE', modelo='User', descripcion='Delete'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('auditoria-stats')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert 'total_logs' in response.data
        assert 'acciones' in response.data
        assert 'modelos' in response.data
        assert 'usuarios_activos' in response.data
        assert response.data['total_logs'] == 3

    def test_stats_action_user(self, api_client, user, audit_log):
        # User should only see their own stats
        api_client.force_authenticate(user=user)
        url = reverse('auditoria-stats')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['total_logs'] == 1  # Only the audit_log fixture

    def test_filtering_by_user(self, api_client, admin_user, user, audit_log):
        other_audit = AuditLog.objects.create(
            usuario=admin_user, accion='LOGIN', modelo='User', descripcion='Login'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('auditoria-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 2  # Both logs since admin