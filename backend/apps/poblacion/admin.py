from django.contrib import admin
from poblacion.models.catalogos import *
from poblacion.models.personas import Persona
from poblacion.models.relaciones import RelacionFamiliar


# Register your models here.
admin.site.register(TipoIdentificacion, NivelEducatico, Ocupacion, GrupoFamiliar,
            EstadoCivil, Lengua, TipoRelacion, Persona, RelacionFamiliar)