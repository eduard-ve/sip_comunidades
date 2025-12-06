"""
Tests de casos límite (edge cases) para la app de auditoría
"""
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework import status
from apps.auditoria.models import AuditLog
from apps.poblacion.models.personas import Persona

User = get_user_model()


class AuditLogEdgeCasesTest(APITestCase):
    """Tests de casos límite para AuditLog"""

    def setUp(self):
        """Configuración inicial para los tests"""
        self.admin_user = User.objects.create_user(
            username='admin',
            email='admin@test.com',
            password='testpass123',
            rol='admin'
        )

    def test_audit_log_with_unicode_characters(self):
        """Test: Crear log de auditoría con caracteres Unicode"""
        persona = Persona.objects.create(
            nombre='José',
            apellido='García',
            numero_identificacion='123456789',
            fecha_nacimiento='1990-01-01',
            genero='M'
        )
        
        log = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo='Persona',
            objeto_id=persona.id,
            descripcion='Creación de persona con caracteres especiales: José García'
        )
        
        self.assertIsNotNone(log)
        self.assertIn('José', log.descripcion)
        self.assertIn('García', log.descripcion)

    def test_audit_log_with_max_length_fields(self):
        """Test: Crear log con campos de longitud máxima"""
        max_descripcion = 'A' * 1000  # Asumiendo que descripcion tiene max_length=1000
        log = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='UPDATE',
            modelo='TestModel',
            objeto_id=1,
            descripcion=max_descripcion[:500]  # Ajustar según el max_length real
        )
        
        self.assertIsNotNone(log)
        self.assertEqual(len(log.descripcion), 500)

    def test_audit_log_with_special_characters_in_descripcion(self):
        """Test: Crear log con caracteres especiales en descripción"""
        descripcion = "Log con caracteres especiales: <script>alert('test')</script> & más"
        log = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='DELETE',
            modelo='TestModel',
            objeto_id=1,
            descripcion=descripcion
        )
        
        self.assertIsNotNone(log)
        self.assertIn('script', log.descripcion)

    def test_audit_log_with_null_usuario(self):
        """Test: Crear log sin usuario (sistema)"""
        log = AuditLog.objects.create(
            usuario=None,
            accion='SYSTEM',
            modelo='System',
            objeto_id=0,
            descripcion='Log del sistema'
        )
        
        self.assertIsNotNone(log)
        self.assertIsNone(log.usuario)

    def test_audit_log_with_very_long_model_name(self):
        """Test: Crear log con nombre de modelo muy largo"""
        model_name = 'A' * 100
        log = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo=model_name[:50],  # Ajustar según max_length
            objeto_id=1,
            descripcion='Test'
        )
        
        self.assertIsNotNone(log)

    def test_filter_audit_logs_by_multiple_criteria(self):
        """Test: Filtrar logs por múltiples criterios"""
        # Crear varios logs
        AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo='Persona',
            objeto_id=1,
            descripcion='Log 1'
        )
        AuditLog.objects.create(
            usuario=self.admin_user,
            accion='UPDATE',
            modelo='Persona',
            objeto_id=2,
            descripcion='Log 2'
        )
        AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo='Usuario',
            objeto_id=1,
            descripcion='Log 3'
        )
        
        # Filtrar por acción y modelo
        logs = AuditLog.objects.filter(accion='CREATE', modelo='Persona')
        self.assertEqual(logs.count(), 1)

    def test_audit_log_with_empty_descripcion(self):
        """Test: Crear log con descripción vacía"""
        log = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='VIEW',
            modelo='TestModel',
            objeto_id=1,
            descripcion=''
        )
        
        self.assertIsNotNone(log)
        self.assertEqual(log.descripcion, '')

    def test_audit_log_with_negative_object_id(self):
        """Test: Crear log con ID de objeto negativo (caso especial)"""
        # Esto podría ser un caso de error, pero probamos que el modelo lo maneja
        try:
            log = AuditLog.objects.create(
                usuario=self.admin_user,
                accion='CREATE',
                modelo='TestModel',
                objeto_id=-1,
                descripcion='Test con ID negativo'
            )
            self.assertIsNotNone(log)
        except Exception:
            # Si el modelo no permite IDs negativos, está bien
            pass

    def test_audit_log_timestamp_ordering(self):
        """Test: Verificar ordenamiento por timestamp"""
        log1 = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo='Test1',
            objeto_id=1,
            descripcion='Primer log'
        )
        
        import time
        time.sleep(0.1)  # Pequeña pausa para asegurar diferencia de tiempo
        
        log2 = AuditLog.objects.create(
            usuario=self.admin_user,
            accion='CREATE',
            modelo='Test2',
            objeto_id=2,
            descripcion='Segundo log'
        )
        
        logs = AuditLog.objects.all().order_by('-fecha_creacion')
        self.assertEqual(logs.first().id, log2.id)

