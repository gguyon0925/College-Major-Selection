# myproject/api/exception_handler.py
from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status, exceptions


def custom_exception_handler(exc, context):
    # Call DRF's default exception handler first
    response = exception_handler(exc, context)

    # Now add custom handling for unauthenticated requests
    if isinstance(exc, exceptions.NotAuthenticated):
        return Response({'detail': 'Authentication credentials were not provided.'}, status=status.HTTP_401_UNAUTHORIZED)

    # If no custom handling was needed, just return the default response
    return response
