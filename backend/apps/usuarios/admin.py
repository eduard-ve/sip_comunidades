from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Usuario

@admin.register(Usuario)
class UsuarioAdmin(UserAdmin):
    # Campos a mostrar en la lista
    list_display = ['username', 'email', 'first_name', 'last_name', 'rol', 'telefono', 'is_active', 'is_staff']
    list_filter = ['rol', 'is_active', 'is_staff', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name', 'telefono']
    ordering = ['-date_joined']
    
    # Configuración de fieldsets para el formulario de edición
    fieldsets = (
        ('Información de Acceso', {
            'fields': ('username', 'email', 'password')
        }),
        ('Información Personal', {
            'fields': ('first_name', 'last_name', 'telefono')
        }),
        ('Permisos y Rol', {
            'fields': ('rol', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')
        }),
        ('Fechas Importantes', {
            'fields': ('last_login', 'date_joined')
        }),
    )
    
    # Campos de solo lectura
    readonly_fields = ['date_joined', 'last_login']
    
    # Configuración para crear nuevo usuario
    add_fieldsets = (
        ('Crear Usuario', {
            'classes': ('wide',),
            'fields': ('username', 'email', 'password1', 'password2', 'first_name', 'last_name', 'telefono', 'rol'),
        }),
    )