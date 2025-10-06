from rest_framework.permissions import BasePermission

class EsAdminRol(BasePermission):
    """Permite acceso solo a usuarios con rol 'admin' o is_staff=True"""
    def has_permission(self, request, view):
        return bool(
            request.user
            and request.user.is_authenticated
            and (request.user.rol == 'admin' or request.user.is_staff)
        )
