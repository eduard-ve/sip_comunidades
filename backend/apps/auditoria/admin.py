from django.contrib import admin
from .models import AuditLog

@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'accion', 'modelo', 'objeto_id', 'fecha')
    list_filter = ('accion', 'modelo', 'fecha', 'usuario')
    search_fields = ('usuario__username', 'modelo', 'descripcion')
    readonly_fields = ('fecha',)
    ordering = ('-fecha',)