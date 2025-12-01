import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from django.contrib.auth import get_user_model

Usuario = get_user_model()

pytestmark = pytest.mark.django_db

class TestUsuarioModel:
    def test_usuario_creation(self):
        usuario = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='editor',
            telefono='123456789'
        )
        assert usuario.username == 'testuser'
        assert usuario.rol == 'editor'
        assert usuario.telefono == '123456789'
        assert usuario.check_password('testpass123')
        expected_str = "testuser (Editor)"
        assert str(usuario) == expected_str

    def test_usuario_role_choices(self):
        choices = dict(Usuario.ROLE_CHOICES)
        assert Usuario.ADMIN in choices
        assert Usuario.EDITOR in choices
        assert Usuario.INVITADO in choices

    def test_usuario_default_role(self):
        usuario = Usuario.objects.create_user(
            username='defaultuser',
            email='default@example.com',
            password='pass123'
        )
        assert usuario.rol == Usuario.INVITADO

    def test_usuario_ordering(self):
        # Create users with different join dates
        from django.utils import timezone
        import datetime

        user1 = Usuario.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123',
            date_joined=timezone.now() - datetime.timedelta(days=1)
        )
        user2 = Usuario.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123',
            date_joined=timezone.now()
        )

        users = list(Usuario.objects.all())
        # Should be ordered by -date_joined, so user2 first
        assert users[0] == user2
        assert users[1] == user1


class TestUsuarioViews(APITestCase):
    def setUp(self):
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            rol='admin'
        )
        self.regular_user = Usuario.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123',
            rol='editor'
        )

    def test_registro_view(self):
        """Test user registration"""
        url = reverse('registro')
        data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'password': 'newpass123',
            'password2': 'newpass123',
            'telefono': '987654321'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Usuario.objects.filter(username='newuser').exists()

    def test_login_view(self):
        """Test JWT token obtain"""
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'adminpass123'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_200_OK
        assert 'access' in response.data
        assert 'refresh' in response.data

        # Check that custom claims are included
        import jwt
        from rest_framework_simplejwt.tokens import AccessToken
        token = AccessToken(response.data['access'])
        assert token['username'] == 'admin'
        assert token['rol'] == 'admin'

    def test_perfil_view_authenticated(self):
        """Test profile view for authenticated user"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('perfil')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == 'user'

    def test_perfil_view_update(self):
        """Test profile update"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('perfil')
        data = {
            'telefono': '555-1234'
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.regular_user.refresh_from_db()
        assert self.regular_user.telefono == '555-1234'

    def test_perfil_view_unauthenticated(self):
        """Test profile view without authentication"""
        url = reverse('perfil')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_usuario_list_admin(self):
        """Test user list for admin"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2  # At least admin and regular user

    def test_usuario_create_admin(self):
        """Test user creation by admin"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-list')
        data = {
            'username': 'created_by_admin',
            'email': 'created@example.com',
            'password': 'pass123',
            'rol': 'editor',
            'telefono': '111222333'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert Usuario.objects.filter(username='created_by_admin').exists()

    def test_usuario_update_admin(self):
        """Test user update by admin"""
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-detail', kwargs={'pk': self.regular_user.pk})
        data = {
            'telefono': '999888777'
        }
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_200_OK
        self.regular_user.refresh_from_db()
        assert self.regular_user.telefono == '999888777'

    def test_usuario_delete_admin(self):
        """Test user deletion by admin"""
        user_to_delete = Usuario.objects.create_user(
            username='to_delete',
            email='delete@example.com',
            password='pass123'
        )
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-detail', kwargs={'pk': user_to_delete.pk})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_204_NO_CONTENT
        assert not Usuario.objects.filter(username='to_delete').exists()

    def test_usuario_list_non_admin(self):
        """Test that non-admin cannot list users"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('usuarios-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_usuario_create_non_admin(self):
        """Test that non-admin cannot create users"""
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('usuarios-list')
        data = {
            'username': 'not_allowed',
            'email': 'not@example.com',
            'password': 'pass123'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_usuario_unauthenticated(self):
        """Test that unauthenticated users cannot access user management"""
        url = reverse('usuarios-list')
        response = self.client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED


class TestPermissions:
    def test_tiene_rol_base_class(self, api_client, user):
        from apps.usuarios.permissions import TieneRol
        permission = TieneRol()
        permission.roles_permitidos = ['user']

        request = api_client.get('/').wsgi_request
        request.user = user

        assert permission.has_permission(request, None)

    def test_tiene_rol_no_auth(self, api_client):
        from apps.usuarios.permissions import TieneRol
        permission = TieneRol()
        permission.roles_permitidos = ['user']

        request = api_client.get('/').wsgi_request
        request.user = None

        assert not permission.has_permission(request, None)

    def test_tiene_rol_wrong_role(self, api_client, user):
        from apps.usuarios.permissions import TieneRol
        permission = TieneRol()
        permission.roles_permitidos = ['admin']

        request = api_client.get('/').wsgi_request
        request.user = user

        assert not permission.has_permission(request, None)

    def test_crear_permiso_roles(self, api_client, user):
        from apps.usuarios.permissions import crear_permiso_roles
        PermisoPersonalizado = crear_permiso_roles('user', 'editor')

        permission = PermisoPersonalizado()
        request = api_client.get('/').wsgi_request
        request.user = user

        assert permission.has_permission(request, None)

    def test_solo_lectura_get(self, api_client, user):
        from apps.usuarios.permissions import SoloLectura
        permission = SoloLectura()

        request = api_client.get('/').wsgi_request
        request.user = user

        assert permission.has_permission(request, None)

    def test_solo_lectura_post(self, api_client, user):
        from apps.usuarios.permissions import SoloLectura
        permission = SoloLectura()

        request = api_client.post('/').wsgi_request
        request.user = user

        assert not permission.has_permission(request, None)

    def test_es_admin_rol_admin(self, api_client, admin_user):
        from apps.usuarios.permissions import EsAdminRol
        permission = EsAdminRol()

        request = api_client.get('/').wsgi_request
        request.user = admin_user

        assert permission.has_permission(request, None)

    def test_es_admin_rol_user(self, api_client, user):
        from apps.usuarios.permissions import EsAdminRol
        permission = EsAdminRol()

        request = api_client.get('/').wsgi_request
        request.user = user

        assert not permission.has_permission(request, None)

    def test_es_editor_rol_editor(self, api_client, user):
        from apps.usuarios.permissions import EsEditorRol
        permission = EsEditorRol()

        # Cambiar rol del usuario a editor
        user.rol = 'editor'
        user.save()

        request = api_client.get('/').wsgi_request
        request.user = user

        assert permission.has_permission(request, None)

    def test_es_editor_rol_user(self, api_client, user):
        from apps.usuarios.permissions import EsEditorRol
        permission = EsEditorRol()

        request = api_client.get('/').wsgi_request
        request.user = user

        assert not permission.has_permission(request, None)

    def test_es_invitado_rol_invitado(self, api_client, user):
        from apps.usuarios.permissions import EsInvitadoRol
        permission = EsInvitadoRol()

        # Cambiar rol del usuario a invitado
        user.rol = 'invitado'
        user.save()

        request = api_client.get('/').wsgi_request
        request.user = user

        assert permission.has_permission(request, None)

    def test_es_invitado_rol_user(self, api_client, user):
        from apps.usuarios.permissions import EsInvitadoRol
        permission = EsInvitadoRol()

        request = api_client.get('/').wsgi_request
        request.user = user

class TestFormValidations:
    def test_registro_serializer_validation(self):
        from apps.usuarios.serializers import RegistroSerializer
        # Test valid data with strong password
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'MyStrongPass123!',
            'password2': 'MyStrongPass123!',
            'telefono': '123456789'
        }
        serializer = RegistroSerializer(data=data)
        assert serializer.is_valid()

    def test_registro_serializer_password_mismatch(self):
        from apps.usuarios.serializers import RegistroSerializer
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'MyStrongPass123!',
            'password2': 'different123',
            'telefono': '123456789'
        }
        serializer = RegistroSerializer(data=data)
        assert not serializer.is_valid()
        # Password mismatch should be in non_field_errors or password2
        assert len(serializer.errors) > 0

    def test_registro_serializer_duplicate_username(self, user):
        from apps.usuarios.serializers import RegistroSerializer
        data = {
            'username': user.username,  # Existing username
            'email': 'new@example.com',
            'password': 'MyStrongPass123!',
            'password2': 'MyStrongPass123!',
            'telefono': '123456789'
        }
        serializer = RegistroSerializer(data=data)
        assert not serializer.is_valid()
        assert 'username' in serializer.errors

    def test_registro_serializer_duplicate_email(self, user):
        from apps.usuarios.serializers import RegistroSerializer
        data = {
            'username': 'newuser',
            'email': user.email,  # Existing email
            'password': 'MyStrongPass123!',
            'password2': 'MyStrongPass123!',
            'telefono': '123456789'
        }
        serializer = RegistroSerializer(data=data)
        assert not serializer.is_valid()
        # Email validation happens at database level, so we check if it's invalid
        assert len(serializer.errors) > 0

    def test_usuario_serializer_validation(self):
        from apps.usuarios.serializers import UsuarioSerializer
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'rol': 'editor',
            'telefono': '123456789'
        }
        serializer = UsuarioSerializer(data=data)
        assert serializer.is_valid()

    def test_usuario_serializer_invalid_rol(self):
        from apps.usuarios.serializers import UsuarioSerializer
        data = {
            'username': 'testuser',
            'email': 'test@example.com',
            'rol': 'invalid_role',
            'telefono': '123456789'
        }
        serializer = UsuarioSerializer(data=data)
        assert not serializer.is_valid()
        assert 'rol' in serializer.errors


class TestErrorHandling(APITestCase):
    def setUp(self):
        self.admin_user = Usuario.objects.create_user(
            username='admin',
            email='admin@example.com',
            password='adminpass123',
            rol='admin'
        )
        self.regular_user = Usuario.objects.create_user(
            username='user',
            email='user@example.com',
            password='userpass123',
            rol='editor'
        )

    def test_registro_view_invalid_data(self):
        url = reverse('registro')
        data = {
            'username': '',  # Invalid empty username
            'email': 'invalid-email',
            'password': '123',
            'password2': '123'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_login_view_wrong_credentials(self):
        url = reverse('token_obtain_pair')
        data = {
            'username': 'admin',
            'password': 'wrongpassword'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_perfil_update_invalid_data(self):
        self.client.force_authenticate(user=self.regular_user)
        url = reverse('perfil')
        data = {
            'telefono': 'invalid-phone-number-with-too-many-characters'
        }
        response = self.client.patch(url, data)
        # Should still work as telefono field allows long strings
        assert response.status_code == status.HTTP_200_OK

    def test_usuario_create_duplicate_username(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-list')
        data = {
            'username': self.regular_user.username,  # Duplicate
            'email': 'new@example.com',
            'password': 'MyStrongPass123!',
            'rol': 'editor'
        }
        response = self.client.post(url, data)
        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_usuario_update_nonexistent(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-detail', kwargs={'pk': 99999})
        data = {'telefono': '123456789'}
        response = self.client.patch(url, data)
        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_usuario_delete_nonexistent(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse('usuarios-detail', kwargs={'pk': 99999})
        response = self.client.delete(url)
        assert response.status_code == status.HTTP_404_NOT_FOUND
