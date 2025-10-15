from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

Usuario = get_user_model()

class UsuariosModuloTests(APITestCase):
    def setUp(self):
        # Crear usuario normal
        self.user = Usuario.objects.create_user(
            username="usuario1",
            email="usuario1@example.com",
            password="Password123!",
            rol=Usuario.INVITADO
        )

        # Crear usuario admin
        self.admin = Usuario.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="Admin123!",
            rol=Usuario.ADMIN,
            is_staff=True
        )

        # Endpoints
        self.register_url = reverse('registro')
        self.login_url = reverse('token_obtain_pair')
        self.perfil_url = reverse('perfil')
        self.usuarios_url = reverse('usuarios-list')

    # -----------------------
    # Registro
    # -----------------------
    def test_registro_usuario_valido(self):
        """Registro de usuario válido"""
        data = {
            "username": "nuevo",
            "email": "nuevo@example.com",
            "password": "Nuevo123!",
            "password2": "Nuevo123!"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Usuario.objects.filter(username="nuevo").exists())

    def test_registro_contrasena_diferente(self):
        """Registro falla si las contraseñas no coinciden"""
        data = {
            "username": "errorpass",
            "email": "error@example.com",
            "password": "Password123!",
            "password2": "Password321!"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("password", response.data)

    # -----------------------
    # Login JWT
    # -----------------------
    def test_login_jwt_valido(self):
        """Login retorna tokens JWT válidos"""
        data = {
            "username": "usuario1",
            "password": "Password123!"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("access", response.data)
        self.assertIn("refresh", response.data)

    def test_login_jwt_invalido(self):
        """Login con credenciales incorrectas falla"""
        data = {
            "username": "usuario1",
            "password": "WrongPass!"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    # -----------------------
    # Perfil
    # -----------------------
    def test_perfil_usuario_autenticado(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.perfil_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["username"], "usuario1")

    # -----------------------
    # Listado de usuarios
    # -----------------------
    def test_listado_usuarios_admin(self):
        token = RefreshToken.for_user(self.admin).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.usuarios_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(response.data), 2)

    def test_listado_usuarios_usuario_normal(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.usuarios_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    # -----------------------
    # Actualización de usuario
    # -----------------------
    def test_actualizar_usuario(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        data = {"first_name": "Eduardo", "telefono": "123456789"}
        response = self.client.patch(self.perfil_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, "Eduardo")
        self.assertEqual(self.user.telefono, "123456789")

    # -----------------------
    # Serialización y campos sensibles
    # -----------------------
    def test_password_no_expuesto(self):
        token = RefreshToken.for_user(self.user).access_token
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(self.perfil_url)
        self.assertNotIn("password", response.data)
        self.assertIn("username", response.data)
        self.assertIn("email", response.data)

    # -----------------------
    # Roles y permisos
    # -----------------------
    def test_rol_por_defecto(self):
        data = {
            "username": "roltest",
            "email": "roltest@example.com",
            "password": "Rol12345!",
            "password2": "Rol12345!"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        usuario = Usuario.objects.get(username="roltest")
        self.assertEqual(usuario.rol, Usuario.INVITADO)
