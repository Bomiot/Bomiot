from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import APIException
from .jwt_auth import parse_payload
from .message import login_message_return


class JwtAuthorizationMiddleware(MiddlewareMixin):
    def process_request(self, request):
        allow_path = ['/', '/login/']
        if request.path_info in allow_path:
            return

        if request.path_info.startswith('/admin/'):
            return

        if request.path_info.startswith('/statics/'):
            return

        if request.path_info.startswith('/js/'):
            return

        if request.path_info.startswith('/css/'):
            return

        if request.path_info.startswith('/assets/'):
            return

        if request.path_info.startswith('/favicon.ico'):
            return

        if request.method == 'OPTIONS':
            return

        token = request.META.get('HTTP_TOKEN', '')
        if token:
            result = parse_payload(token).get('status')
            if result is True:
                return
            else:
                raise APIException(login_message_return(request.META.get('HTTP_LANGUAGE', ''), 'Please Login Again'))
        else:
            return
