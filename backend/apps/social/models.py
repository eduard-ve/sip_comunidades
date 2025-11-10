from django.db import models
from apps.poblacion.models.personas import Persona
from apps.usuarios.models import Usuario

# Constantes para textos repetitivos
VERBOSE_NAME_DESCRIPCION = "Descripción"

# Modelos para gestión de autoridades y líderes comunitarios
class TipoAutoridad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Tipo de Autoridad")
    descripcion = models.TextField(blank=True, verbose_name=VERBOSE_NAME_DESCRIPCION)

    class Meta:
        verbose_name = "Tipo de Autoridad"
        verbose_name_plural = "Tipos de Autoridad"

    def __str__(self):
        return self.nombre


class RolAutoridad(models.Model):
    nombre = models.CharField(max_length=100, unique=True, verbose_name="Rol")
    descripcion = models.TextField(blank=True, verbose_name=VERBOSE_NAME_DESCRIPCION)

    class Meta:
        verbose_name = "Rol de Autoridad"
        verbose_name_plural = "Roles de Autoridad"

    def __str__(self):
        return self.nombre


class AutoridadComunitaria(models.Model):
    persona = models.OneToOneField(Persona, on_delete=models.CASCADE, verbose_name="Persona")
    tipo_autoridad = models.ForeignKey(TipoAutoridad, on_delete=models.PROTECT, verbose_name="Tipo de Autoridad")
    rol = models.ForeignKey(RolAutoridad, on_delete=models.PROTECT, verbose_name="Rol")
    fecha_inicio_mandato = models.DateField(verbose_name="Fecha Inicio Mandato")
    fecha_fin_mandato = models.DateField(null=True, blank=True, verbose_name="Fecha Fin Mandato")
    telefono_contacto = models.CharField(max_length=20, blank=True, verbose_name="Teléfono de Contacto")
    email_contacto = models.EmailField(blank=True, verbose_name="Email de Contacto")
    observaciones = models.TextField(blank=True, verbose_name="Observaciones")
    activo = models.BooleanField(default=True, verbose_name="Activo")

    class Meta:
        verbose_name = "Autoridad Comunitaria"
        verbose_name_plural = "Autoridades Comunitarias"
        ordering = ['persona__primer_apellido', 'persona__primer_nombre']

    def __str__(self):
        return f"{self.persona} - {self.rol} ({self.tipo_autoridad})"


# Modelo para gestionar programas sociales y sus beneficiarios
class EstadoPrograma(models.Model):
    nombre = models.CharField(max_length=50, unique=True)

    class Meta:
        verbose_name = "Estado del Programa"
        verbose_name_plural = "Estados de los Programas"

    def __str__(self):
        return self.nombre


class ProgramaSocial(models.Model):  # modelo principal de programas sociales
    nombre = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    estado = models.ForeignKey(EstadoPrograma, on_delete=models.PROTECT)
    fecha_inicio = models.DateField(null=True, blank=True)
    fecha_fin = models.DateField(null=True, blank=True)
    beneficiarios = models.ManyToManyField(Persona, related_name='programas_sociales', blank=True)
    beneficiarios_count = models.PositiveIntegerField(default=0, verbose_name="Cantidad de Beneficiarios")
    responsable = models.ForeignKey(Usuario, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        verbose_name = "Programa Social"
        verbose_name_plural = "Programas Sociales"

    def __str__(self):
        return self.nombre


class ProgramaBeneficiario(models.Model):  # intermediario para gestionar beneficiarios de programas sociales
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('egresado', 'Egresado'),
    ]

    programa = models.ForeignKey(ProgramaSocial, on_delete=models.CASCADE)
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE)
    fecha_inscripcion = models.DateField(auto_now_add=True)
    observaciones = models.TextField(blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='activo')
    fecha_egreso = models.DateField(null=True, blank=True)

    class Meta:
        verbose_name = "Beneficiario de Programa"
        verbose_name_plural = "Beneficiarios de Programas"
        unique_together = ('programa', 'persona')

    def save(self, *args, **kwargs):
        """Sincroniza el ManyToMany al guardar un beneficiario"""
        super().save(*args, **kwargs)
        if self.persona not in self.programa.beneficiarios.all():
            self.programa.beneficiarios.add(self.persona)

    def __str__(self):
        return f"{self.persona} - {self.programa}"


class ActividadSocial(models.Model):  # modelo para actividades relacionadas con programas sociales
    programa = models.ForeignKey(ProgramaSocial, null=True, blank=True, on_delete=models.SET_NULL)
    titulo = models.CharField(max_length=150)
    descripcion = models.TextField(blank=True)
    fecha = models.DateField(null=True, blank=True)
    ubicacion = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name = "Actividad Social"
        verbose_name_plural = "Actividades Sociales"

    def __str__(self):
        return self.titulo


class CoberturaPrograma(models.Model):  # modelo para definir áreas de cobertura de programas sociales
    programa = models.ForeignKey(ProgramaSocial, on_delete=models.CASCADE)
    latitud = models.DecimalField(max_digits=10, decimal_places=6)
    longitud = models.DecimalField(max_digits=10, decimal_places=6)
    descripcion = models.CharField(max_length=225, blank=True)
    area_nombre = models.CharField(max_length=100, blank=True)

    class Meta:
        verbose_name = "Cobertura de Programa"
        verbose_name_plural = "Coberturas de Programa"

    def __str__(self):
        return f"{self.programa.nombre} - {self.area_nombre or 'Área sin nombre'}"
