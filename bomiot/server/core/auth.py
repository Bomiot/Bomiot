from django.contrib.auth import get_user_model
from rest_framework.exceptions import APIException
from .message import login_message_return
from .jwt_auth import parse_payload
import typing

User = get_user_model()


class CoreAuthentication:
    """
    custom authenticate
    """

    def authenticate(self, request) -> typing.Tuple[bool, typing.Union[User, None]]:
        """
        auth user request
        :param request: HTTP request
        :return: (auth status, user)
        """
        # path that does not require authentication
        if request.path in ['/', '/api/docs/', '/api/debug/', '/api/', '/core/user/permission/']:
            return False, None

        # get request Token
        token = request.META.get('HTTP_TOKEN', '')
        if not token:
            self._raise_api_exception(request, 'Please Login First')

        # parse Token
        result = parse_payload(token)
        if result.get('status') is False:
            self._raise_api_exception(request, 'Please Login Again')
        user_id = result.get('data', {}).get('id')
        user_permissions = result.get('data', {}).get('permission', {})

        # authenticate user
        user = User.objects.filter(id=user_id, is_delete=False).first()
        if not user:
            self._raise_api_exception(request, "User not exists")

        # authenticate user status
        if not user.is_active:
            self._raise_api_exception(request, 'User is not active')

        # authenticate user permissions
        if sorted(user.permission.items()) != sorted(user_permissions.items()):
            self._raise_api_exception(request, 'Please Login Again')

        return True, user

    def authenticate_header(self, request) -> None:
        """
        authenticate header
        :param request: HTTP request
        """
        pass

    @staticmethod
    def _raise_api_exception(request, message: str) -> None:
        """
        Raise APIException exception
        :param request: HTTP request
        :param message: exception message
        """
        language = request.META.get('HTTP_LANGUAGE', '')
        raise APIException(login_message_return(language, message))