from rest_framework import viewsets, permissions
from poblacion.models.personas import Persona
from poblacion.serializers.personas import PersonaSerializer
from usuarios.permissions import EsAdminRol

# Vista genérica para el modelo Persona
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
