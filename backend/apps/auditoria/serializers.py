from rest_framework import serializers
from .models import AuditLog

class AuditLogSerializer(serializers.ModelSerializer):
    usuario_username = serializers.SerializerMethodField()
    usuario_rol = serializers.SerializerMethodField()

    def get_usuario_username(self, obj):
        return obj.usuario.username if obj.usuario else ''

    def get_usuario_rol(self, obj):
        return obj.usuario.rol if obj.usuario else ''

    class Meta:
        model = AuditLog
        fields = [
            'id_audit', 'usuario', 'usuario_username', 'usuario_rol',
            'accion', 'modelo', 'objeto_id', 'descripcion',
            'ip_address', 'fecha', 'datos_anteriores', 'datos_nuevos'
        ]
        read_only_fields = ['id_audit', 'fecha']