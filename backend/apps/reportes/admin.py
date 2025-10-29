from django.contrib import admin
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas

@admin.register(ReporteSalud)
class ReporteSaludAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_reporte', 'fecha_reporte', 'generado_por', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'tipo_reporte')
    ordering = ('-fecha_reporte',)

@admin.register(ReporteSocial)
class ReporteSocialAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_reporte', 'fecha_reporte', 'generado_por', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'tipo_reporte')
    ordering = ('-fecha_reporte',)

@admin.register(ReporteEncuestas)
class ReporteEncuestasAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_reporte', 'fecha_reporte', 'generado_por', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'tipo_reporte')
    ordering = ('-fecha_reporte',)
