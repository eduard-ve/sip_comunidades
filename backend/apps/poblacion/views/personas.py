from rest_framework import viewsets, permissions
from ..models.personas import Persona
from ..serializers.personas import PersonaSerializer
from apps.usuarios.permissions import EsAdminRol


class PersonaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar las operaciones CRUD del modelo Persona.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
