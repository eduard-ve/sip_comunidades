from django.contrib import admin
from .models import ReporteSalud, ReporteSocial, ReporteEncuestas

@admin.register(ReporteSalud)
class ReporteSaludAdmin(admin.ModelAdmin):
    list_display = ('generado_por', 'tipo_reporte', 'fecha_reporte', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte', 'generado_por')
    search_fields = ('generado_por__username', 'generado_por__first_name', 'generado_por__last_name', 'tipo_reporte')
    ordering = ('-fecha_reporte',)

@admin.register(ReporteSocial)
class ReporteSocialAdmin(admin.ModelAdmin):
    list_display = ('generado_por', 'tipo_reporte', 'fecha_reporte', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte', 'generado_por')
    search_fields = ('generado_por__username', 'generado_por__first_name', 'generado_por__last_name', 'tipo_reporte')
    ordering = ('-fecha_reporte',)

@admin.register(ReporteEncuestas)
class ReporteEncuestasAdmin(admin.ModelAdmin):
    list_display = ('generado_por', 'tipo_reporte', 'fecha_reporte', 'fecha_creacion')
    list_filter = ('tipo_reporte', 'fecha_reporte', 'generado_por')
    search_fields = ('generado_por__username', 'generado_por__first_name', 'generado_por__last_name', 'tipo_reporte')
    ordering = ('-fecha_reporte',)
