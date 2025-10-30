from rest_framework import viewsets
from ..models import ProgramaBeneficiario, ActividadSocial, CoberturaPrograma
from ..serializers.beneficiarios import (
    ProgramaBeneficiarioSerializer,
    ActividadSocialSerializer,
    CoberturaProgramaSerializer,
)

# ViewSet para el modelo ProgramaBeneficiario
class ProgramaBeneficiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar beneficiarios de programas sociales.
    """
    queryset = ProgramaBeneficiario.objects.select_related('programa', 'persona').all()
    serializer_class = ProgramaBeneficiarioSerializer


# ViewSet para el modelo ActividadSocial
class ActividadSocialViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar actividades sociales.
    """
    queryset = ActividadSocial.objects.select_related('programa').all()
    serializer_class = ActividadSocialSerializer


# ViewSet para el modelo CoberturaPrograma
class CoberturaProgramaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar coberturas geográficas de los programas sociales.
    """
    queryset = CoberturaPrograma.objects.select_related('programa').all()
    serializer_class = CoberturaProgramaSerializer
