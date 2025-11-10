from django.core.management.base import BaseCommand
from apps.social.models import TipoAutoridad, RolAutoridad, AutoridadComunitaria
from apps.poblacion.models.personas import Persona


class Command(BaseCommand):
    help = 'Crea datos iniciales para autoridades comunitarias'

    def handle(self, *args, **options):
        self.stdout.write('Creando datos iniciales para autoridades comunitarias...\n')

        # Crear tipos de autoridad
        tipos_data = [
            {'nombre': 'Tradicional', 'descripcion': 'Autoridad tradicional comunitaria'},
            {'nombre': 'Comunitaria', 'descripcion': 'Autoridad elegida por la comunidad'},
        ]

        for tipo_data in tipos_data:
            tipo, created = TipoAutoridad.objects.get_or_create(
                nombre=tipo_data['nombre'],
                defaults={'descripcion': tipo_data['descripcion']}
            )
            if created:
                self.stdout.write(f'Creado tipo de autoridad: {tipo.nombre}')
            else:
                self.stdout.write(f'Tipo ya existe: {tipo.nombre}')

        # Crear roles de autoridad
        roles_data = [
            {'nombre': 'Coordinador', 'descripcion': 'Coordinador general'},
            {'nombre': 'Secretario', 'descripcion': 'Secretario administrativo'},
            {'nombre': 'Tesorero', 'descripcion': 'Responsable de finanzas'},
        ]

        for rol_data in roles_data:
            rol, created = RolAutoridad.objects.get_or_create(
                nombre=rol_data['nombre'],
                defaults={'descripcion': rol_data['descripcion']}
            )
            if created:
                self.stdout.write(f'Creado rol de autoridad: {rol.nombre}')
            else:
                self.stdout.write(f'Rol ya existe: {rol.nombre}')

        # Crear algunas autoridades de ejemplo si hay personas
        if Persona.objects.exists():
            tipos = list(TipoAutoridad.objects.all())
            roles = list(RolAutoridad.objects.all())

            if tipos and roles:
                # Tomar las primeras 3 personas que no sean autoridades activas
                personas_disponibles = Persona.objects.exclude(
                    autoridadcomunitaria__activo=True
                )[:3]

                for i, persona in enumerate(personas_disponibles):
                    tipo = tipos[i % len(tipos)]
                    rol = roles[i % len(roles)]

                    autoridad, created = AutoridadComunitaria.objects.get_or_create(
                        persona=persona,
                        defaults={
                            'tipo_autoridad': tipo,
                            'rol': rol,
                            'fecha_inicio_mandato': '2024-01-01',
                            'telefono_contacto': f'300{i+1}234567',
                            'email_contacto': f'autoridad{i+1}@example.com',
                            'activo': True
                        }
                    )
                    if created:
                        self.stdout.write(f'Creada autoridad: {autoridad.persona.nombre_completo}')
                    else:
                        self.stdout.write(f'Autoridad ya existe: {autoridad.persona.nombre_completo}')

        self.stdout.write('\nProceso completado exitosamente!')
        self.stdout.write(f'Resumen:')
        self.stdout.write(f'   - Tipos de autoridad: {TipoAutoridad.objects.count()}')
        self.stdout.write(f'   - Roles de autoridad: {RolAutoridad.objects.count()}')
        self.stdout.write(f'   - Autoridades comunitarias: {AutoridadComunitaria.objects.count()}')