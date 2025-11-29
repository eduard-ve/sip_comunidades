from django.db import models
from apps.usuarios.models import Usuario

# Modelo para reportes de salud
class ReporteSalud(models.Model):
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte (ej: resumen salud, indicadores)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['generado_por', 'tipo_reporte', 'fecha_reporte']

    def __str__(self):
        return f"Reporte Salud - {self.tipo_reporte} ({self.fecha_reporte}) - {self.generado_por}"

    class Meta:
        verbose_name = "Reporte de Salud"
        verbose_name_plural = "Reportes de Salud"
        ordering = ['-fecha_reporte']

# Modelo para reportes sociales
class ReporteSocial(models.Model):
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte social (ej: apoyo social, condiciones)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte social en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['generado_por', 'tipo_reporte', 'fecha_reporte']

    def __str__(self):
        return f"Reporte Social - {self.tipo_reporte} ({self.fecha_reporte}) - {self.generado_por}"

    class Meta:
        verbose_name = "Reporte Social"
        verbose_name_plural = "Reportes Sociales"
        ordering = ['-fecha_reporte']

# Modelo para reportes de encuestas
class ReporteEncuestas(models.Model):
    tipo_reporte = models.CharField(max_length=100, help_text="Tipo de reporte de encuestas (ej: resultados encuesta, análisis)")
    datos_agregados = models.JSONField(help_text="Datos agregados del reporte de encuestas en formato JSON")
    fecha_reporte = models.DateField()
    generado_por = models.CharField(max_length=100, help_text="Usuario que generó el reporte")
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_modificacion = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ['generado_por', 'tipo_reporte', 'fecha_reporte']

    def __str__(self):
        return f"Reporte Encuestas - {self.tipo_reporte} ({self.fecha_reporte}) - {self.generado_por}"

    class Meta:
        verbose_name = "Reporte de Encuestas"
        verbose_name_plural = "Reportes de Encuestas"
        ordering = ['-fecha_reporte']
