from rest_framework.permissions import BasePermission, SAFE_METHODS

class TieneRol(BasePermission):
    """
    Permite acceso solo a usuarios con uno de los roles especificados.
    Uso:
        permission_classes = [TieneRol('admin', 'editor')]
    """

    def __init__(self, *roles_permitidos):
        self.roles_permitidos = roles_permitidos

    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.rol in self.roles_permitidos
                or request.user.is_staff
            )
        )

# Permisos específicos
class SoloLectura(BasePermission):
    """
    Permite acceso de solo lectura (GET, HEAD, OPTIONS).
    Ideal para endpoints públicos.
    """
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

# Permisos personalizados
class EsAdmin(BasePermission):
    """Permite acceso solo a administradores."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (request.user.rol == 'admin' or request.user.is_staff)
        )

# Permisos personalizados
class EsEditor(BasePermission):
    """Permite acceso a administradores y editores."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and (
                request.user.rol in ['admin', 'editor']
                or request.user.is_staff
            )
        )

# Permisos personalizados
class EsInvitado(BasePermission):
    """Permite acceso solo a usuarios con rol 'invitado'."""
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.is_authenticated
            and request.user.rol == 'invitado'
        )
