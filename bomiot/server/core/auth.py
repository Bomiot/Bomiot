from rest_framework.exceptions import APIException
from .jwt_auth import parse_payload
from django.contrib.auth import get_user_model

User = get_user_model()

class AsyncAuthentication(object):
    async def authenticate(self, request) -> tuple[User, bool]:
        if request.path in ['/docs/', '/swagger/']:
            return (False, False)
        else:
            token = request.META.get('HTTP_TOKEN', '')
            result = parse_payload(token)
            if token:
                user_data = await User.objects.filter(id=result.get('data').aget('id'))
                if user_data.exists():
                    user = user_data.afirst()
                    return (user, True)
                else:
                    raise APIException({"msg": "User Does Not Exists"})
            else:
                raise APIException({"msg": "Please Add Token To Your Request Headers"})

    async def authenticate_header(self, request):
        pass
