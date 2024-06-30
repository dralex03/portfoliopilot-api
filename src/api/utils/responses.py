from typing import Dict, Any, List

from flask import make_response, jsonify

from src.api.utils import jwt_auth
from src.constants import http_status_codes as status



def generate_success_response(response: List[Dict[str, Any]] | Dict[str, Any] | str):
    """
    Generates a flask response for successful requests.
    Parameters:
        List[Dict[str, Any]] | Dict[str, Any] | str response;
    Returns:
        tuple:
            Response: Flask Response, contains the response_object dict
            int: the response status code
    """
    response_object = {
        'success': True,
        'response': response
    }
    return make_response(jsonify(response_object)), status.HTTP_200_OK


def generate_internal_error_response(message: str, error: Exception | str):
    """
    Generates a flask response for internal server errors.
    Parameters:
        str message;
        Exception | str error;
    Returns:
        tuple:
            Response: Flask Response, contains the response_object dict
            int: the response status code
    """
    response_object = {
        'success': False,
        'message': message,
        'error': str(error)
    }
    return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR


def generate_bad_request_response(message: str):
    """
    Generates a flask response for bad requests.
    Parameters:
        str message;
    Returns:
        tuple:
            Response: Flask Response, contains the response_object dict
            int: the response status code
    """
    response_object = {
        'success': False,
        'message': message
    }
    return make_response(jsonify(response_object)), status.HTTP_400_BAD_REQUEST


def generate_not_found_response(message: str):
    """
    Generates a flask response for not found (404).
    Parameters:
        str message;
    Returns:
        tuple:
            Response: Flask Response, contains the response_object dict
            int: the response status code
    """
    response_object = {
        'success': False,
        'message': message
    }
    return make_response(jsonify(response_object)), status.HTTP_404_NOT_FOUND


def generate_auth_token_response(user_id: str, success_message: str):
    """
    Generate an authentication token for a given user ID and return the appropriate Flask response.
    Parameters:
        str user_id;
        str success_message;
        int success_status;
    Returns:
        tuple:
            Response: Flask Response, contains the response_object dict
            int: the response status code
    """
    auth_token = jwt_auth.encode_auth_token(user_id)

    if not auth_token:
        return generate_internal_error_response('Error generating Auth Token.', 'Unknown error occurred.')
    
    response = {
        'message': success_message,
        'auth_token': auth_token
    }
    return generate_success_response(response)