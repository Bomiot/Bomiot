from django.contrib.auth import get_user_model

User = get_user_model()


class AsyncPermission:
    async def has_permission(self, request, view) -> bool:
        return bool(request.user and request.user.is_authenticated)

    async def has_object_permission(self, request, view, obj):
        if obj.user == request.user or request.user.is_superuser:
            return True
        return False