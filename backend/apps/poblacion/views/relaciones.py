from rest_framework import viewsets, permissions
from poblacion.models.relaciones import RelacionFamiliar
from poblacion.serializers.relaciones import RelacionFamiliarSerializer
from usuarios.permissions import EsAdminRol

# Vista genérica para el modelo RelacionFamiliar
class RelacionFamiliarViewSet(viewsets.ModelViewSet):
    queryset = RelacionFamiliar.objects.all()
    serializer_class = RelacionFamiliarSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
