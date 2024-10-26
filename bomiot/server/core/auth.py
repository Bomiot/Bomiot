from rest_framework.exceptions import APIException
from .jwt_auth import parse_payload
from django.contrib.auth import get_user_model

User = get_user_model()

class AsyncAuthentication(object):
    def authenticate(self, request) -> tuple[User, bool]:
        print(request.path)
        if request.path in ['/', '/docs/', '/swagger/']:
            return (False, False)
        else:
            token = request.META.get('HTTP_TOKEN', '')
            result = parse_payload(token)
            if token:
                try:
                    user_data = User.objects.aget(id=result.get('data', '').get('id', ''))
                except:
                    raise APIException({"msg": "User Does Not Exists"})
                finally:
                    return (user_data, True)
            else:
                raise APIException({"msg": "Please Add Token To Your Request Headers"})

    def authenticate_header(self, request):
        pass
