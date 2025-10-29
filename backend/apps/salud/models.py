from django.db import models
from apps.poblacion.models.personas import Persona

# Modelo para registros de salud
class RegistroSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='registros_salud')
    fecha_registro = models.DateField()
    tipo_registro = models.CharField(max_length=100, help_text="Tipo de registro (ej: consulta, vacunación)")
    descripcion = models.TextField(blank=True, null=True)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Registro de {self.persona} - {self.tipo_registro} ({self.fecha_registro})"

    class Meta:
        verbose_name = "Registro de Salud"
        verbose_name_plural = "Registros de Salud"
        ordering = ['-fecha_registro']

# Modelo para alertas de salud
class AlertaSalud(models.Model):
    PRIORIDAD_CHOICES = [
        ('baja', 'Baja'),
        ('media', 'Media'),
        ('alta', 'Alta'),
        ('critica', 'Crítica'),
    ]

    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='alertas_salud')
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    prioridad = models.CharField(max_length=10, choices=PRIORIDAD_CHOICES, default='media')
    fecha_alerta = models.DateField(auto_now_add=True)
    resuelta = models.BooleanField(default=False)
    fecha_resolucion = models.DateField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Alerta para {self.persona} - {self.titulo} ({self.prioridad})"

    class Meta:
        verbose_name = "Alerta de Salud"
        verbose_name_plural = "Alertas de Salud"
        ordering = ['-fecha_alerta']

# Modelo para controles de salud
class ControlSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='controles_salud')
    tipo_control = models.CharField(max_length=100, help_text="Tipo de control (ej: vacunación, chequeo)")
    fecha_programada = models.DateField()
    fecha_realizada = models.DateField(blank=True, null=True)
    realizado = models.BooleanField(default=False)
    observaciones = models.TextField(blank=True, null=True)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Control de {self.persona} - {self.tipo_control} ({self.fecha_programada})"

    class Meta:
        verbose_name = "Control de Salud"
        verbose_name_plural = "Controles de Salud"
        ordering = ['fecha_programada']
