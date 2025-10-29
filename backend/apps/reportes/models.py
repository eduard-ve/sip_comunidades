from django.db import models
from apps.poblacion.models.personas import Persona

# Modelo para reportes de salud
class ReporteSalud(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='reportes_salud')
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte (ej: resumen salud, indicadores)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reporte Salud de {self.persona} - {self.tipo_reporte} ({self.fecha_reporte})"

    class Meta:
        verbose_name = "Reporte de Salud"
        verbose_name_plural = "Reportes de Salud"
        ordering = ['-fecha_reporte']

# Modelo para reportes sociales
class ReporteSocial(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='reportes_sociales')
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte social (ej: apoyo social, condiciones)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte social en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reporte Social de {self.persona} - {self.tipo_reporte} ({self.fecha_reporte})"

    class Meta:
        verbose_name = "Reporte Social"
        verbose_name_plural = "Reportes Sociales"
        ordering = ['-fecha_reporte']

# Modelo para reportes de encuestas
class ReporteEncuestas(models.Model):
    persona = models.ForeignKey(Persona, on_delete=models.CASCADE, related_name='reportes_encuestas')
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte de encuestas (ej: resultados encuesta, análisis)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte de encuestas en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reporte Encuestas de {self.persona} - {self.tipo_reporte} ({self.fecha_reporte})"

    class Meta:
        verbose_name = "Reporte de Encuestas"
        verbose_name_plural = "Reportes de Encuestas"
        ordering = ['-fecha_reporte']
