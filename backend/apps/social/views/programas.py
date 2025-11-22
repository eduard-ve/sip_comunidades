from rest_framework import viewsets, permissions
from ..models import EstadoPrograma, ProgramaSocial
from ..serializers.programas import EstadoProgramaSerializer, ProgramaSocialSerializer
from apps.usuarios.permissions import EsAdminRol

# ViewSet para el modelo EstadoPrograma
class EstadoProgramaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar estados de programas sociales.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = EstadoPrograma.objects.all()
    serializer_class = EstadoProgramaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]


# ViewSet para el modelo ProgramaSocial
class ProgramaSocialViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar programas sociales.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = ProgramaSocial.objects.select_related('estado').all()
    serializer_class = ProgramaSocialSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
