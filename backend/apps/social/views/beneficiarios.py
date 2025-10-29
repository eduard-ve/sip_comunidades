from rest_framework import  viewsets
from ..models import ProgramaBeneficiario, ActividadSocial, CoberturaPrograma
from ..serializers.beneficiarios import ProgramaBeneficiarioSerializer, ActividadSocialSerializer, CoberturaProgramaSerializer

# ViewSet para el modelo ProgramaBeneficiario
class ProgramaBeneficiarioViewSet(viewsets.ModelViewSet):
    queryset = ProgramaBeneficiario.objects.select_related('programa', 'persona').all()
    serializer_class = ProgramaBeneficiarioSerializer

# ViewSet para el modelo ActividadSocial
class ActividadSocialViewSet(viewsets.ModelViewSet):
    queryset = ActividadSocial.objects.select_related('programa').all()
    serializer_class = ActividadSocialSerializer

# ViewSet para el modelo CoberturaPrograma
class CoberturaProgramaViewSet(viewsets.ModelViewSet):
    queryset = CoberturaPrograma.objects.select_related('programa').all()
    serializer_class = CoberturaProgramaSerializer
    