from django.contrib.auth.models import AbstractUser
from django.db import models

class Usuario(AbstractUser):
    # Campo de teléfono
    telefono = models.CharField(max_length=20, blank=True, null=True, help_text="Número de teléfono del usuario"
    )
    
    # Definir choices como constantes
    ADMIN = 'admin'
    EDITOR = 'editor'
    INVITADO = 'invitado'
    
    ROLE_CHOICES = [
        (ADMIN, 'Administrador'),
        (EDITOR, 'Editor'),
        (INVITADO, 'Invitado'),
    ]
    
    # Campo de rol
    rol = models.CharField(max_length=50, choices=ROLE_CHOICES, default=INVITADO, help_text="Rol del usuario en el sistema"
    )
    
    # Fecha de creación
    def __str__(self):
        return f"{self.username} ({self.get_rol_display()})"
    
    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ['-date_joined']