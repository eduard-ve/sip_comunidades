from rest_framework import viewsets, permissions
from ..models.relaciones import RelacionFamiliar
from ..serializers.relaciones import RelacionFamiliarSerializer
from apps.usuarios.permissions import EsAdminRol

# Vista genérica para el modelo RelacionFamiliar
class RelacionFamiliarViewSet(viewsets.ModelViewSet):
    queryset = RelacionFamiliar.objects.all()
    serializer_class = RelacionFamiliarSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
