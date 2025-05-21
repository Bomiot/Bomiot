from django.contrib.auth import get_user_model
from bomiot.server.core.utils import contains_value


User = get_user_model()


class BasePermission:
    """
    Base permission class
    """
    def has_permission(self, request, view) -> bool:
        raise NotImplementedError("need has_permission function")


class CorePermission(BasePermission):
    """
    core permission class, check if user has permission to access the path
    """
    def has_permission(self, request, view) -> bool:
        if request.user:
            return contains_value(request.auth.permission, request.path)
        return False


class NormalPermission(BasePermission):
    """
    normal permission class, allow all users to access the path
    """
    def has_permission(self, request, view) -> bool:
        return True