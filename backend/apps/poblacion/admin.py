from django.contrib import admin
from apps.poblacion.models.catalogos import *
from apps.poblacion.models.personas import Persona
from apps.poblacion.models.relaciones import RelacionFamiliar


# Register your models here.
admin.site.register(TipoIdentificacion)
admin.site.register(NivelEducatico)
admin.site.register(Ocupacion)
admin.site.register(GrupoFamiliar)
admin.site.register(EstadoCivil)
admin.site.register(Lengua)
admin.site.register(TipoRelacion)
admin.site.register(Persona)
admin.site.register(RelacionFamiliar)