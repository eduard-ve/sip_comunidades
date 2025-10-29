from django.db import models
from .catalogos import (
    TipoIdentificacion, NivelEducatico, Ocupacion, GrupoFamiliar,
    EstadoCivil, Lengua, TipoRelacion
)

# Modelo de Persona
class Persona(models.Model):
    # Opciones de género
    GENERO_CHOICES = [
        ('M', 'Maculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
    ]
    
    tipo_identificacion = models.ForeignKey(TipoIdentificacion, on_delete=models.PROTECT)
    numero_identificacion = models.CharField(max_length=50, unique=True)
    primer_nombre = models.CharField(max_length=100)
    segundo_nombre = models.CharField(max_length=100, blank=True, null=True)
    primer_apellido = models.CharField(max_length=100)
    segundo_apellido = models.CharField(max_length=100,blank=True, null=True)
    fecha_nacimiento = models.DateField()
    genero = models.CharField(max_length=1, choices=GENERO_CHOICES)
    direccion = models.CharField(max_length=255,blank=True, null=True)
    nivel_educativo = models.ForeignKey(NivelEducatico, on_delete=models.SET_NULL, null=True, blank=True)
    ocupacion = models.ForeignKey(Ocupacion, on_delete=models.SET_NULL, null=True, blank=True)
    grupo_familiar = models.ForeignKey(GrupoFamiliar, on_delete=models.SET_NULL, null=True, blank=True)
    estado_civil = models.ForeignKey(EstadoCivil, on_delete=models.SET_NULL, null=True, blank=True)
    lengua_materna = models.ForeignKey(Lengua, on_delete=models.SET_NULL, null=True, blank=True)

    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.primer_nombre} {self.primer_apellido} - {self.numero_identificacion}"
    
    # Meta información
    class Meta:
        verbose_name = "Persona"
        verbose_name_plural = "Personas"
        ordering = ['primer_apellido', 'primer_nombre']


