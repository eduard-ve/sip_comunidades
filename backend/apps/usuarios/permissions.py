from rest_framework.permissions import BasePermission, SAFE_METHODS


class TieneRol(BasePermission):
    """
    Permite acceso solo a usuarios con uno de los roles especificados.
    Uso recomendado:
        Crear subclases o usar la función factory `crear_permiso_roles()`.
    """

    roles_permitidos = []

    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and hasattr(user, "rol")
            and (
                user.rol in self.roles_permitidos
                or user.is_staff
            )
        )


def crear_permiso_roles(*roles):
    """
    Crea una clase de permiso personalizada para los roles indicados.
    Ejemplo:
        EsAdminOEditor = crear_permiso_roles('admin', 'editor')
        permission_classes = [permissions.IsAuthenticated, EsAdminOEditor]
    """
    class PermisoDinamico(TieneRol):
        roles_permitidos = roles
    return PermisoDinamico


class SoloLectura(BasePermission):
    """Permite acceso de solo lectura (GET, HEAD, OPTIONS)."""
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS


class EsAdminRol(BasePermission):
    """Permite acceso solo a usuarios con rol 'admin' o staff."""
    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and hasattr(user, "rol")
            and (user.rol == "admin" or user.is_staff)
        )


class EsEditorRol(BasePermission):
    """Permite acceso a administradores y editores."""
    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and hasattr(user, "rol")
            and (user.rol in ["admin", "editor"] or user.is_staff)
        )


class EsInvitadoRol(BasePermission):
    """Permite acceso solo a usuarios con rol 'invitado'."""
    def has_permission(self, request, view):
        user = request.user
        return (
            user
            and user.is_authenticated
            and hasattr(user, "rol")
            and user.rol == "invitado"
        )
