from rest_framework import viewsets, permissions
from apps.poblacion.models.personas import Persona
from apps.poblacion.serializers.personas import PersonaSerializer
from apps.usuarios.permissions import EsAdmin

# Vista genérica para el modelo Persona
class PersonaViewSet(viewsets.ModelViewSet):
    queryset = Persona.objects.all()
    serializer_class = PersonaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdmin]
