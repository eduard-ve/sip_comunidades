from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Count
from django.db.models.functions import ExtractYear
from datetime import datetime
from .models import RegistroSalud, AlertaSalud, ControlSalud, HistorialMedico, Vacuna, Medicamento, ExamenMedico
from .serializers import (
    RegistroSaludSerializer, AlertaSaludSerializer, ControlSaludSerializer,
    HistorialMedicoSerializer, VacunaSerializer, MedicamentoSerializer, ExamenMedicoSerializer
)
from apps.usuarios.permissions import EsAdminRol
from apps.poblacion.models.personas import Persona

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

# Vista para Estadísticas de Salud
class SaludStatsViewSet(viewsets.ViewSet):
    """
    ViewSet para estadísticas de salud
    """
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['get'])
    def enfermedades_comunes(self, request):
        """
        Enfermedades más comunes basadas en registros de salud
        """
        enfermedades = RegistroSalud.objects.values('tipo_registro').annotate(
            count=Count('tipo_registro')
        ).order_by('-count')[:10]

        data = []
        for enf in enfermedades:
            data.append({
                'enfermedad': enf['tipo_registro'],
                'casos': enf['count']
            })

        return Response(data)

    @action(detail=False, methods=['get'])
    def distribucion_edad_salud(self, request):
        """
        Distribución por grupos de edad de registros de salud
        """
        current_year = datetime.now().year
        rangos = [
            ('Niños', 0, 12),
            ('Adolescentes', 13, 17),
            ('Adultos', 18, 64),
            ('Adultos mayores', 65, 120)
        ]

        data = []
        for nombre, min_edad, max_edad in rangos:
            count = RegistroSalud.objects.filter(
                persona__fecha_nacimiento__isnull=False
            ).annotate(
                edad=current_year - ExtractYear('persona__fecha_nacimiento')
            ).filter(edad__gte=min_edad, edad__lte=max_edad).count()

            data.append({
                'grupo': nombre,
                'cantidad': count
            })

        return Response(data)

    @action(detail=False, methods=['get'])
    def kpis_salud(self, request):
        """
        KPIs principales de salud
        """
        registros_count = RegistroSalud.objects.count()
        alertas_activas = AlertaSalud.objects.filter(resuelta=False).count()
        controles_pendientes = ControlSalud.objects.filter(realizado=False).count()
        controles_realizados = ControlSalud.objects.filter(realizado=True).count()

        return Response({
            'registros_salud': registros_count,
            'alertas_activas': alertas_activas,
            'controles_pendientes': controles_pendientes,
            'controles_realizados': controles_realizados
        })

# Vista para Historiales Médicos
class HistorialMedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar historiales médicos.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = HistorialMedico.objects.all()
    serializer_class = HistorialMedicoSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Vacunas
class VacunaViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar vacunas.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = Vacuna.objects.all()
    serializer_class = VacunaSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Medicamentos
class MedicamentoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar medicamentos.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = Medicamento.objects.all()
    serializer_class = MedicamentoSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]

# Vista para Exámenes Médicos
class ExamenMedicoViewSet(viewsets.ModelViewSet):
    """
    ViewSet para gestionar exámenes médicos.
    Solo accesible para usuarios autenticados con rol de administrador.
    """
    queryset = ExamenMedico.objects.all()
    serializer_class = ExamenMedicoSerializer
    permission_classes = [permissions.IsAuthenticated, EsAdminRol]
