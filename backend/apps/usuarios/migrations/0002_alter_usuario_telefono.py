# Generated migration for alterar telefono max_length
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usuario',
            name='telefono',
            field=models.CharField(blank=True, help_text='Número de teléfono del usuario', max_length=255, null=True),
        ),
    ]