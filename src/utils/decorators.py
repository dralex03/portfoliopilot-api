from functools import wraps
from typing import Callable

from flask import Blueprint, request, make_response, jsonify

from src.constants.http_status_codes import HTTP_401_UNAUTHORIZED
from src.utils.jwt_auth import decode_auth_token
from src.database.queries import get_user_by_id

def jwt_required(func: Callable):
    """
    Wrapper function for every API request that requires user authentication.
        Parameters:
            function func;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
            OR: executes the wrapped function
    """

    @wraps(func)
    def decorator(*args, **kwargs):
        response_object = {}

        # Get Auth header from the request object
        auth_header = request.headers.get('Authorization')
    
        # Check if auth_header is in correct format and extract the JWT
        if auth_header and auth_header.startswith('Bearer '):
            auth_token = auth_header.split(' ')[1]
        else:
            auth_token = ''

        if auth_token:
            # Decode the JWT
            is_valid, uid_or_message = decode_auth_token(auth_token)
            
            if is_valid:
                # If the token is valid, make sure the user exists
                user = get_user_by_id(uid_or_message)

                # If user exists, continue with wrapped function
                if user:
                    return func(user_id=uid_or_message, *args, **kwargs)
                else:
                    response_object = {
                        'success': False,
                        'message': 'User does not exist.'
                    }
            else:
                response_object = {
                    'success': False,
                    'message': uid_or_message
                }
        else:
            response_object = {
                'success': False,
                'message': 'Missing JWT auth-token or invalid format.'
            }

        return make_response(jsonify(response_object)), HTTP_401_UNAUTHORIZED
        
    return decorator