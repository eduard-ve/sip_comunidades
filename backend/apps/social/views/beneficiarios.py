from rest_framework import viewsets, permissions
from ..models import ProgramaBeneficiario, ActividadSocial, CoberturaPrograma
from ..serializers.beneficiarios import (
    ProgramaBeneficiarioSerializer,
    ActividadSocialSerializer,
    CoberturaProgramaSerializer,
)
from apps.usuarios.permissions import EsAdminRol

# ViewSet para el modelo ProgramaBeneficiario
class ProgramaBeneficiarioViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar beneficiarios de programas sociales.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = ProgramaBeneficiario.objects.select_related('programa', 'persona').all()
    serializer_class = ProgramaBeneficiarioSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]


# ViewSet para el modelo ActividadSocial
class ActividadSocialViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar actividades sociales.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = ActividadSocial.objects.select_related('programa').all()
    serializer_class = ActividadSocialSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]


# ViewSet para el modelo CoberturaPrograma
class CoberturaProgramaViewSet(viewsets.ModelViewSet):
    """
    API endpoint para gestionar coberturas geográficas de los programas sociales.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = CoberturaPrograma.objects.select_related('programa').all()
    serializer_class = CoberturaProgramaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
