from django.contrib.auth import get_user_model

User = get_user_model()


class AsyncPermission:
    def has_permission(self, request, view) -> bool:
        return True
        # return bool(request.user and request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return True
        # if obj.user == request.user or request.user.is_superuser:
        #     return True
        # return False