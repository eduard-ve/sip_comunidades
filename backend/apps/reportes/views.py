from rest_framework import viewsets, permissions
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas
from .serializers import ReporteSaludSerializer, ReporteSocialSerializer, ReporteEncuestasSerializer
from apps.usuarios.permissions import EsAdminRol

# Vista para Reportes de Salud
class ReporteSaludViewSet(viewsets.ModelViewSet):
    queryset = ReporteSalud.objects.all()
    serializer_class = ReporteSaludSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Reportes Sociales
class ReporteSocialViewSet(viewsets.ModelViewSet):
    queryset = ReporteSocial.objects.all()
    serializer_class = ReporteSocialSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Reportes de Encuestas
class ReporteEncuestasViewSet(viewsets.ModelViewSet):
    queryset = ReporteEncuestas.objects.all()
    serializer_class = ReporteEncuestasSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
