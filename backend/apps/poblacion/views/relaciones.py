from rest_framework import viewsets, permissions
from apps.poblacion.models.relaciones import RelacionFamiliar
from apps.poblacion.serializers.relaciones import RelacionFamiliarSerializer
from apps.usuarios.permissions import EsAdmin

# Vista genérica para el modelo RelacionFamiliar
class RelacionFamiliarViewSet(viewsets.ModelViewSet):
    queryset = RelacionFamiliar.objects.all()
    serializer_class = RelacionFamiliarSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdmin]
