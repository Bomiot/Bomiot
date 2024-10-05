from django.shortcuts import render
from rest_framework.decorators import api_view, permission_classes



@api_view(['GET'])
def index(request):
    """
    render index page
    :param request: request object
    :return: page
    """
    return render(request, 'index.html')

