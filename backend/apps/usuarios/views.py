from rest_framework import generics, permissions, viewsets
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .serializers import RegistroSerializer, UsuarioSerializer
from .permissions import EsAdminRol

Usuario = get_user_model()

#Registro de usuario
class RegistroView(generics.CreateAPIView):
    queryset = Usuario.objects.all()
    serializer_class = RegistroSerializer
    permission_classes = [permissions.AllowAny]

#Login con JWT
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Agregar info adicional al token
        token['username'] = user.username
        token['rol'] = user.rol
        return token

    def validate(self, attrs):
        data = super().validate(attrs)
        # Agregar info del usuario al access token también
        user = self.user
        # Crear access token con la info adicional
        from rest_framework_simplejwt.tokens import AccessToken
        access_token = AccessToken.for_user(user)
        access_token['username'] = user.username
        access_token['rol'] = user.rol
        data['access'] = str(access_token)
        return data

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Perfil del usuario autenticado
class PerfilView(generics.RetrieveUpdateAPIView):
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Vista para gestionar usuarios (CRUD completo para admin)
class UsuarioViewSet(viewsets.ModelViewSet):
    queryset = Usuario.objects.all()
    serializer_class = UsuarioSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

