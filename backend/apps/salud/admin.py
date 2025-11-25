from django.contrib import admin
from .models import RegistroSalud, AlertaSalud, ControlSalud, HistorialMedico, Vacuna, Medicamento, ExamenMedico

@admin.register(RegistroSalud)
class RegistroSaludAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_registro', 'fecha_registro', 'fecha_creacion')
    list_filter = ('tipo_registro', 'fecha_registro')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'tipo_registro')
    ordering = ('-fecha_registro',)

@admin.register(AlertaSalud)
class AlertaSaludAdmin(admin.ModelAdmin):
    list_display = ('persona', 'titulo', 'prioridad', 'resuelta', 'fecha_alerta')
    list_filter = ('prioridad', 'resuelta', 'fecha_alerta')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'titulo')
    ordering = ('-fecha_alerta',)

@admin.register(ControlSalud)
class ControlSaludAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_control', 'fecha_programada', 'realizado', 'fecha_realizada')
    list_filter = ('tipo_control', 'realizado', 'fecha_programada')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'tipo_control')
    ordering = ('fecha_programada',)

@admin.register(HistorialMedico)
class HistorialMedicoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'fecha_creacion')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido')
    ordering = ('-fecha_creacion',)

@admin.register(Vacuna)
class VacunaAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nombre_vacuna', 'tipo_vacuna', 'fecha_aplicacion')
    list_filter = ('tipo_vacuna', 'fecha_aplicacion')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'nombre_vacuna')
    ordering = ('-fecha_aplicacion',)

@admin.register(Medicamento)
class MedicamentoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'nombre_medicamento', 'fecha_prescripcion', 'activo')
    list_filter = ('activo', 'fecha_prescripcion')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'nombre_medicamento')
    ordering = ('-fecha_prescripcion',)

@admin.register(ExamenMedico)
class ExamenMedicoAdmin(admin.ModelAdmin):
    list_display = ('persona', 'tipo_examen', 'nombre_examen', 'fecha_solicitud')
    list_filter = ('tipo_examen', 'fecha_solicitud')
    search_fields = ('persona__primer_nombre', 'persona__primer_apellido', 'nombre_examen')
    ordering = ('-fecha_solicitud',)
