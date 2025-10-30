from rest_framework import viewsets
from ..models import EstadoPrograma, ProgramaSocial
from ..serializers.programas import EstadoProgramaSerializer, ProgramaSocialSerializer

# ViewSet para el modelo EstadoPrograma
class EstadoProgramaViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar estados de programas sociales.
    """
    queryset = EstadoPrograma.objects.all()
    serializer_class = EstadoProgramaSerializer


# ViewSet para el modelo ProgramaSocial
class ProgramaSocialViewSet(viewsets.ModelViewSet):
    """
    API endpoint que permite ver o editar programas sociales.
    """
    queryset = ProgramaSocial.objects.select_related('estado').all()
    serializer_class = ProgramaSocialSerializer
