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

        # Handle plural to singular conversion for model names
        if model_class_name.endswith('es') and model_class_name[-3:] != 'les':
            # Remove 'es' for most cases (e.g., EstadosCiviles -> EstadoCivil)
            model_class_name = model_class_name[:-2]
        elif model_class_name.endswith('s'):
            # Remove 's' for regular plurals (e.g., Lenguas -> Lengua)
            model_class_name = model_class_name[:-1]

        return getattr(catalogos, model_class_name)\
            .objects.all().order_by('nombre')
