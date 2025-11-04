from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from apps.auditoria.models import AuditLog
from datetime import timedelta
from django.utils import timezone

User = get_user_model()

class Command(BaseCommand):
    help = 'Crear datos de auditoría de ejemplo'

    def handle(self, *args, **options):
        # Obtener usuarios existentes
        admin_user = User.objects.filter(rol='admin').first()
        editor_user = User.objects.filter(rol='editor').first()
        invitado_user = User.objects.filter(rol='invitado').first()

        if not admin_user:
            self.stdout.write(self.style.WARNING('No hay usuario admin. Ejecuta create_users primero.'))
            return

        # Crear logs de auditoría de ejemplo
        audit_logs = [
            {
                'usuario': admin_user,
                'accion': 'LOGIN',
                'modelo': 'Usuario',
                'objeto_id': str(admin_user.id),
                'descripcion': f'Inicio de sesión del usuario {admin_user.username}',
                'ip_address': '192.168.1.100',
                'fecha': timezone.now() - timedelta(hours=2)
            },
            {
                'usuario': admin_user,
                'accion': 'CREATE',
                'modelo': 'Encuesta',
                'objeto_id': '1',
                'descripcion': 'Creación de nueva encuesta: Satisfacción del cliente',
                'ip_address': '192.168.1.100',
                'fecha': timezone.now() - timedelta(hours=1, minutes=30)
            },
            {
                'usuario': editor_user,
                'accion': 'UPDATE',
                'modelo': 'Persona',
                'objeto_id': '5',
                'descripcion': 'Actualización de datos personales',
                'ip_address': '192.168.1.101',
                'fecha': timezone.now() - timedelta(hours=1)
            },
            {
                'usuario': admin_user,
                'accion': 'DELETE',
                'modelo': 'ProgramaSocial',
                'objeto_id': '2',
                'descripcion': 'Eliminación de programa social inactivo',
                'ip_address': '192.168.1.100',
                'fecha': timezone.now() - timedelta(minutes=45)
            },
            {
                'usuario': invitado_user,
                'accion': 'VIEW',
                'modelo': 'Reporte',
                'objeto_id': '3',
                'descripcion': 'Visualización de reporte de salud',
                'ip_address': '192.168.1.102',
                'fecha': timezone.now() - timedelta(minutes=30)
            },
            {
                'usuario': editor_user,
                'accion': 'CREATE',
                'modelo': 'ControlSalud',
                'objeto_id': '10',
                'descripcion': 'Registro de nuevo control de salud',
                'ip_address': '192.168.1.101',
                'fecha': timezone.now() - timedelta(minutes=15)
            },
            {
                'usuario': admin_user,
                'accion': 'UPDATE',
                'modelo': 'Usuario',
                'objeto_id': str(editor_user.id),
                'descripcion': f'Cambio de rol del usuario {editor_user.username}',
                'ip_address': '192.168.1.100',
                'fecha': timezone.now() - timedelta(minutes=10)
            },
            {
                'usuario': invitado_user,
                'accion': 'VIEW',
                'modelo': 'Encuesta',
                'objeto_id': '1',
                'descripcion': 'Acceso a encuesta activa',
                'ip_address': '192.168.1.102',
                'fecha': timezone.now() - timedelta(minutes=5)
            }
        ]

        # Crear los logs
        for log_data in audit_logs:
            AuditLog.objects.get_or_create(
                usuario=log_data['usuario'],
                accion=log_data['accion'],
                modelo=log_data['modelo'],
                objeto_id=log_data['objeto_id'],
                descripcion=log_data['descripcion'],
                defaults={
                    'ip_address': log_data['ip_address'],
                    'fecha': log_data['fecha']
                }
            )

        self.stdout.write(
            self.style.SUCCESS(f'Se crearon {len(audit_logs)} registros de auditoría de ejemplo')
        )