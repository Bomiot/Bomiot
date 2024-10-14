from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import DatabaseError


async def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    if response is not None:
        response.data['status_code'] = response.status_code
        response = Response(response.data)
    else:
        if isinstance(exc, DatabaseError):
            response = Response({'msg': DatabaseError})
        else:
            response = Response({'msg': 'Other Error'})
    return response
