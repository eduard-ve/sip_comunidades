from django.contrib import admin
from apps.poblacion.models.catalogos import *
from apps.poblacion.models.personas import Persona
from apps.poblacion.models.relaciones import RelacionFamiliar


# Registro de los modelos de población en el admin de Django
admin.site.register(TipoIdentificacion)
admin.site.register(NivelEducativo)
admin.site.register(Ocupacion)
admin.site.register(GrupoEtnico)
admin.site.register(EstadoCivil)
admin.site.register(Lengua)
admin.site.register(TipoRelacion)
admin.site.register(Persona)
admin.site.register(RelacionFamiliar)