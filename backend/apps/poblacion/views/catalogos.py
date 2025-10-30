from rest_framework import viewsets, permissions
from ..serializers.catalogos import CatalogoSerializer
from ..models import catalogos

# crear un viewset generico para los catalogos
class CatalogoViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = CatalogoSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        model_name = self.basename  # ejemplo. 'tipos_identificacion'
        model_class_name = ''.join(word.capitalize() for word in model_name.split('_'))
        return getattr(catalogos, model_class_name)\
            .objects.all().order_by('nombre')
