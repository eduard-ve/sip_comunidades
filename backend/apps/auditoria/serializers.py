from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    usuario_username = serializers.CharField(source='usuario.username', read_only=True)
    usuario_rol = serializers.CharField(source='usuario.rol', read_only=True)

    class Meta:
        model = AuditLog
        fields = [
            'id_audit', 'usuario', 'usuario_username', 'usuario_rol',
            'accion', 'modelo', 'objeto_id', 'descripcion',
            'ip_address', 'fecha', 'datos_anteriores', 'datos_nuevos'
        ]
        read_only_fields = ['id_audit', 'fecha']