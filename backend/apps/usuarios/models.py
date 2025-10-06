from django.contrib.auth.models import AbstractUser
from django.db import models

# Clase personalizada de usuario
class Usuario(AbstractUser):
    telefono = models.CharField(max_length=20, blank=True, null=True, help_text="Número de teléfono del usuario")
 
#definir choices como constantes
ADMIN = 'admin'
EDITOR = 'editor'
INVITADO = 'invitado'

ROLE_CHOICES = [
    (ADMIN, 'Administrador'),   
    (EDITOR, 'Editor'),
    (INVITADO, 'Invitado'),
]
role = models.CharField(max_length=50, choices=ROLE_CHOICES, default=INVITADO, help_text="Rol del usuario en el sistema")

#funcion que retorna el nombre del usuario
def __str__(self):
    return self.username

class Meta:
    verbose_name = "Usuario"
    verbose_name_plural = "Usuarios"
    ordering = ['-date_joined']#ordenar por fecha de creacion, el mas reciente primero