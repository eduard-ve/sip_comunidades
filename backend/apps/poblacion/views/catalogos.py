from rest_framework import viewsets, permissions
from apps.poblacion.serializers.catalogos import CatalogoSerializer
from apps.poblacion.models import catalogos

# crear un viewset generico para los catalogos
class CatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CatalogoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        model_name = self.basename  # ejempo. 'tipos_identificacion'
        return getattr(catalogos, model_name.capitalize().replace('_', ''))\
            .objects.all().order_by('nombre')
