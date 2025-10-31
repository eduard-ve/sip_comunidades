from rest_framework.permissions import BasePermission

# Permiso personalizado para verificar si el usuario es el creador de la encuesta
class EsCreadorEncuesta(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Solo el creador de la encuesta puede editar
        return hasattr(obj, 'creada_por') and obj.creada_por == request.user
