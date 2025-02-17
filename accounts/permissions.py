from rest_framework.permissions import BasePermission


class UsuarioPermission(BasePermission):
    def has_permission(self, request, view):
        return bool(
            request.method not in ("PUT", "DELETE")
            or request.user
            and request.user.is_authenticated
        )
