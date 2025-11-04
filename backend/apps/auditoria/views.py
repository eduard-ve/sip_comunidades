from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.filters import OrderingFilter
from django.db.models import Count
from .models import AuditLog
from .serializers import AuditLogSerializer

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.all()
    serializer_class = AuditLogSerializer
    permission_classes = [permissions.IsAuthenticated]
    filter_backends = [OrderingFilter]
    ordering_fields = ['fecha', 'usuario', 'accion']
    ordering = ['-fecha']

    def get_queryset(self):
        queryset = super().get_queryset()
        # Solo admins pueden ver todos los logs
        if not self.request.user.rol == 'admin':
            queryset = queryset.filter(usuario=self.request.user)
        return queryset

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """Estadísticas de auditoría"""
        queryset = self.get_queryset()

        stats = {
            'total_logs': queryset.count(),
            'acciones': queryset.values('accion').annotate(count=Count('accion')).order_by('-count'),
            'modelos': queryset.values('modelo').annotate(count=Count('modelo')).order_by('-count'),
            'usuarios_activos': queryset.values('usuario__username').distinct().count()
        }

        return Response(stats)