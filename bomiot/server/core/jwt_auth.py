import jwt
import datetime
from django.conf import settings

# from settings import JWT_SALT 
JWT_SALT = getattr(settings, "JWT_SALT", settings.SECRET_KEY)


def create_token(payload):
    """
    create JWT Token
    :param payload: JWT Token data
    :return: JWT Token
    """
    headers = {
        "type": "JWT",
        "alg": "HS256"
    }
    # set Token outtime
    payload['exp'] = datetime.datetime.now() + datetime.timedelta(seconds=settings.USER_JWT_TIME)
    # create Token
    token = jwt.encode(payload=payload, key=JWT_SALT, algorithm="HS256", headers=headers)
    return token


def parse_payload(token):
    """
    parse JWT Token
    :param token: JWT Token
    :return: include status, data, error
    """
    result = {"status": False, "data": None, "error": None}
    try:
        # verify Token and decode payload
        verified_payload = jwt.decode(token, JWT_SALT, algorithms="HS256", options={"verify_exp": True})
        result["status"] = True
        result['data'] = verified_payload
    except jwt.ExpiredSignatureError:
        result['detail'] = 'Token Expired'
    except jwt.DecodeError:
        result['detail'] = 'Token Authentication Failed'
    except jwt.InvalidTokenError:
        result['detail'] = 'Illegal Token'
    except Exception as e:
        result['detail'] = f"Unknown error: {str(e)}"
    return result