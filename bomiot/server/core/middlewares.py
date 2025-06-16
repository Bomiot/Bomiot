from .jwt_auth import parse_payload
from .message import login_message_return
from rest_framework.exceptions import APIException
from django.utils.deprecation import MiddlewareMixin


class JwtAuthorizationMiddleware(MiddlewareMixin):
    """
    JWT Middleware
    """
    # allowed paths and prefixes
    ALLOWED_PATHS = [
        '/',
        '/login/',
        '/favicon.ico',
    ]
    ALLOWED_PREFIXES = [
        '/admin/',
        '/statics/',
        '/js/',
        '/css/',
        '/assets/',
    ]
    ALLOWED_METHODS = ['OPTIONS']

    def process_request(self, request):
        """
        auth request JWT Token
        :param request: HTTP request
        """
        if self._is_allowed_path(request) or request.method in self.ALLOWED_METHODS:
            return

        token = request.META.get('HTTP_TOKEN', '')
        if token:
            result = parse_payload(token).get('status')
            if result is True:
                return
            else:
                raise APIException(
                    login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login Again')
                )
        else:
            raise APIException(
                login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login First')
            )

    def _is_allowed_path(self, request):
        """
        check if the request path is allowed
        :param request: HTTP request
        :return: bool
        """
        if request.path_info in self.ALLOWED_PATHS:
            return True
        for prefix in self.ALLOWED_PREFIXES:
            if request.path_info.startswith(prefix):
                return True
        return False
    

class DisableMediaCachingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        if request.path.startswith('/media/'):
            response['Cache-Control'] = 'no-cache, no-store, must-revalidate'
            response['Pragma'] = 'no-cache'
            response['Expires'] = '0'
        return response