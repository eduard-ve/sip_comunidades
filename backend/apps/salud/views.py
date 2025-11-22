from rest_framework import viewsets, permissions
from .models import RegistroSalud, AlertaSalud, ControlSalud
from .serializers import RegistroSaludSerializer, AlertaSaludSerializer, ControlSaludSerializer
from apps.usuarios.permissions import EsAdminRol

# Vista para Registros de Salud
class RegistroSaludViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar registros de salud.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = RegistroSalud.objects.all()
    serializer_class = RegistroSaludSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Alertas de Salud
class AlertaSaludViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar alertas de salud.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = AlertaSalud.objects.all()
    serializer_class = AlertaSaludSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Controles de Salud
class ControlSaludViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar controles de salud.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = ControlSalud.objects.all()
    serializer_class = ControlSaludSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
