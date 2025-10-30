from django.db import models

# Base asbtract class para catálogos
class CatalogoBase(models.Model):
    nombre = models.CharField(max_length=100,unique=True)

    class Meta:
        abstract = True
        ordering = ['nombre']

    def __str__(self):
        return self.nombre
    
# Catálogos específicos de la aplicación de población 
class TipoIdentificacion(CatalogoBase):
    class Meta:
        verbose_name = "Tipo de Identificación"
        verbose_name_plural = "Tipos de Identificación"

class NivelEducativo(CatalogoBase):
    class Meta:
        verbose_name = "Nivel Educativo"
        verbose_name_plural = "Niveles Educativos"

class Ocupacion(CatalogoBase):
    class Meta:
        verbose_name = "Ocupación"
        verbose_name_plural = "Ocupaciones"

class GrupoFamiliar(CatalogoBase):
    class Meta:
        verbose_name = "Grupo Familiar"
        verbose_name_plural = "Grupos Familiares"

class EstadoCivil(CatalogoBase):
    class Meta:
        verbose_name = "Estado Civil"
        verbose_name_plural = "Estados Civiles"

class Lengua(CatalogoBase):
    class Meta:
        verbose_name = "Lengua"
        verbose_name_plural = "Lenguas"

class TipoRelacion(CatalogoBase):
    class Meta:
        verbose_name = "Tipo de Relación"
        verbose_name_plural = "Tipos de Relaciones"



