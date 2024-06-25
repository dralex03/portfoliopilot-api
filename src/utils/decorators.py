from functools import wraps
from typing import Callable, List
import inspect

from flask import request, make_response, jsonify

from src.constants.http_status_codes import HTTP_401_UNAUTHORIZED
from src.utils.jwt_auth import decode_auth_token
from src.utils.responses import *
from src.database import queries, models
from src.constants import http_status_codes as status


def validate_function_params(func: Callable, required_params: List[str]):
    """
    Validator function that checks whether a decorated function signature includes
    requires parameters that are passed on by the decorator.
        Parameters:
            function func;
            List[str] required_params;
        Returns:
            None
        Raises:
            TypeError: If the function signature does not include the required parameters.
    """
    func_params = inspect.signature(func).parameters

    missing_params = [p for p in required_params if p not in func_params]
    if missing_params:
        raise TypeError(f"Function '{func.__name__}' missing required parameters: {missing_params}")


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
        # Ensure the decorated function includes the passed on parameters
        validate_function_params(func, ['user_id'])

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
                user = queries.get_user_by_id(uid_or_message)

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


def validate_portfolio_owner(func: Callable):
    """
    Wrapper function for every API request that includes a portfolio_id to check
    that the user_id from authentication is the owner of this portfolio.

    Needs to be used in combination with @jwt_required decorator, in the following order:
    @jwt_required
    @validate_portfolio_owner
    def function(...)

        Parameters:
            function func;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
            OR: executes the wrapped function
    """

    @wraps(func)
    def decorator(user_id: str, portfolio_id: str, *args, **kwargs):
        # Ensure the decorated function includes the passed on parameters
        validate_function_params(func, ['user_id', 'portfolio'])

        # Fetch portfolio by portfolio ID
        try:
            portfolio: models.Portfolio = queries.get_portfolio_by_id(portfolio_id)
        except Exception as e:
            return generate_internal_error_response(f'Error fetching portfolio with ID "{portfolio_id}".', e)
        
        # Check whether the user owns this portfolio or not
        if str(portfolio.user_id) == user_id:
            return func(user_id=user_id, portfolio=portfolio, *args, **kwargs)
        else:
            response_object = {
                'success': False,
                'message': f'Portfolio with ID "{portfolio_id}" does not belong to User "{user_id}"'
            }
            return make_response(jsonify(response_object)), status.HTTP_403_FORBIDDEN
        
    return decorator