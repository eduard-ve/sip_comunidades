from django.contrib import admin
from .models import EstadoPrograma, ProgramaSocial, ProgramaBeneficiario, ActividadSocial, CoberturaPrograma

# registro de los modelos en el admin de Django
admin.site.register(EstadoPrograma)
admin.site.register(ProgramaSocial)
admin.site.register(ProgramaBeneficiario)
admin.site.register(ActividadSocial)
admin.site.register(CoberturaPrograma)