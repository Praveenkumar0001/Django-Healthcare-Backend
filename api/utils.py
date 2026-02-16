from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    """
    Custom exception handler for REST Framework.
    Provides consistent error response format across the API.
    """
    # Call REST framework's default exception handler first
    response = exception_handler(exc, context)

    if response is not None:
        # Customize the response data
        custom_response_data = {
            'success': False,
            'error': {
                'message': None,
                'details': None
            }
        }

        # Handle different types of errors
        if isinstance(response.data, dict):
            if 'detail' in response.data:
                custom_response_data['error']['message'] = response.data['detail']
            else:
                custom_response_data['error']['message'] = 'Validation error'
                custom_response_data['error']['details'] = response.data
        elif isinstance(response.data, list):
            custom_response_data['error']['message'] = response.data[0] if response.data else 'An error occurred'
        else:
            custom_response_data['error']['message'] = str(response.data)

        response.data = custom_response_data

    return response


def success_response(data=None, message="Success", status_code=status.HTTP_200_OK):
    """
    Helper function to create standardized success responses.
    """
    return Response({
        'success': True,
        'message': message,
        'data': data
    }, status=status_code)


def error_response(message="An error occurred", details=None, status_code=status.HTTP_400_BAD_REQUEST):
    """
    Helper function to create standardized error responses.
    """
    return Response({
        'success': False,
        'error': {
            'message': message,
            'details': details
        }
    }, status=status_code)
