from rest_framework.views import exception_handler
from rest_framework.response import Response
from django.db import DatabaseError


def custom_exception_handler(exc, context):
    """
    custom exception handler for DRF
    :param exc: exception 
    :param context: context information
    :return: Response
    """
    # use DRF's default exception handler to get the standard error response
    response = exception_handler(exc, context)

    if response is not None:
        # add additional information to the response
        response.data['status_code'] = response.status_code
        response = Response(response.data)
    else:
        # handle the exception
        print(exc, DatabaseError)
        if isinstance(exc, DatabaseError):
            response = Response({'msg': 'A database error occurred.'})
        else:
            # handle other exceptions
            # response = Response({'msg': 'An unknown error occurred.'})
            pass

    return response