from django.contrib import admin
from .models import RegistroSalud, AlertaSalud, ControlSalud

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
