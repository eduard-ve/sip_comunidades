import pytest
from django.urls import reverse
from rest_framework import status
from apps.usuarios.models import Usuario

pytestmark = pytest.mark.django_db

class TestUsuarioModel:
    def test_usuario_creation(self):
        user = Usuario.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            rol='editor',
            telefono='123456789'
        )
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.rol == 'editor'
        assert user.telefono == '123456789'
        assert user.is_active is True

    def test_usuario_str(self):
        user = Usuario.objects.create_user(
            username='johndoe',
            email='john@example.com',
            password='pass123',
            rol='admin'
        )
        expected = "johndoe (Administrador)"
        assert str(user) == expected

    def test_usuario_role_choices(self):
        choices = dict(Usuario.ROLE_CHOICES)
        assert 'admin' in choices
        assert 'editor' in choices
        assert 'invitado' in choices

    def test_usuario_default_role(self):
        user = Usuario.objects.create_user(
            username='defaultuser',
            email='default@example.com',
            password='pass123'
        )
        assert user.rol == 'invitado'

    def test_usuario_ordering(self):
        user1 = Usuario.objects.create_user(
            username='user1',
            email='user1@example.com',
            password='pass123'
        )
        user2 = Usuario.objects.create_user(
            username='user2',
            email='user2@example.com',
            password='pass123'
        )
        # Should be ordered by -date_joined, so user2 first
        users = list(Usuario.objects.all())
        assert users[0] == user2
        assert users[1] == user1


class TestUsuarioViewSet:
    def test_list_usuarios_admin(self, api_client, admin_user):
        Usuario.objects.create_user(
            username='testuser2',
            email='test2@example.com',
            password='pass123'
        )
        api_client.force_authenticate(user=admin_user)
        url = reverse('usuario-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) >= 2  # At least admin and testuser2

    def test_create_usuario_admin(self, api_client, admin_user):
        api_client.force_authenticate(user=admin_user)
        data = {
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'newpass123',
            'rol': 'editor',
            'telefono': '987654321'
        }
        url = reverse('usuario-list')
        response = api_client.post(url, data)
        assert response.status_code == status.HTTP_201_CREATED
        assert response.data['username'] == 'newuser'

    def test_retrieve_usuario_admin(self, api_client, admin_user, user):
        api_client.force_authenticate(user=admin_user)
        url = reverse('usuario-detail', kwargs={'pk': user.pk})
        response = api_client.get(url)
        assert response.status_code == status.HTTP_200_OK
        assert response.data['username'] == user.username

    def test_unauthenticated_access(self, api_client):
        url = reverse('usuario-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_non_admin_access(self, api_client, user):
        api_client.force_authenticate(user=user)
        url = reverse('usuario-list')
        response = api_client.get(url)
        assert response.status_code == status.HTTP_403_FORBIDDEN
