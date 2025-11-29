from django.core.management.base import BaseCommand
from apps.social.models import ProgramaBeneficiario


class Command(BaseCommand):
    help = 'Sincroniza los beneficiarios ManyToMany en ProgramaSocial'

    def handle(self, *args, **options):
        self.stdout.write('Sincronizando beneficiarios ManyToMany...\n')

        beneficiarios = ProgramaBeneficiario.objects.all()
        synced = 0

        for beneficiario in beneficiarios:
            if beneficiario.persona not in beneficiario.programa.beneficiarios.all():
                beneficiario.programa.beneficiarios.add(beneficiario.persona)
                synced += 1
                self.stdout.write(f'Agregado {beneficiario.persona} a {beneficiario.programa}')

        # Actualizar contadores
        for programa in beneficiario.programa.__class__.objects.all():
            programa.beneficiarios_count = programa.beneficiarios.count()
            programa.save(update_fields=['beneficiarios_count'])

        self.stdout.write(f'\nProceso completado! {synced} beneficiarios sincronizados.')