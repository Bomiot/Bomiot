from django.contrib.auth import get_user_model
from bomiot.server.core.utils import contains_value


User = get_user_model()


class CorePermission:
    def has_permission(self, request, view) -> bool:
        if request.user:
            return contains_value(request.auth.permission, request.path)
        else:
            return False

class NormalPermission:
    def has_permission(self, request, view) -> bool:
        return True