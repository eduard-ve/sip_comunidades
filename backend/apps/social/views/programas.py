from rest_framework import viewsets
from ..models import EstadoPrograma, ProgramaSocial
from ..serializers.programas import EstadoProgramaSerializer, ProgramaSocialSerializer

# ViewSet para el modelo EstadoPrograma
class EstadoProgramaViewSet(viewsets.ModelViewSet):
    queryset = EstadoPrograma.objects.all()
    serializer_class = EstadoProgramaSerializer

# ViewSet para el modelo ProgramaSocial
class ProgramaSocialViewSet(viewsets.ModelViewSet):
    queryset = ProgramaSocial.objects.select_related('estado').all()
    serializer_class = ProgramaSocialSerializer