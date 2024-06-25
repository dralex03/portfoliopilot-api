import bcrypt
from flask import Blueprint, request, make_response, jsonify

from src.database import queries
from src.utils.input_validation import is_valid_email, is_strong_password
from src.constants import http_status_codes as status
from src.utils.decorators import jwt_required
from src.utils.responses import *
from src.routes.user_portfolios import user_portfolios

# Create blueprint which is used in the flask app
user = Blueprint('user', __name__)

user.register_blueprint(user_portfolios, url_prefix='/portfolios')


@user.route('/register', methods = ['POST'])
def register():
    """
    Handles POST requests to /user/register 
        Parameters:
            -
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Parsing the request body
    request_body = request.get_json()
    user_email = request_body.get('email')
    user_password = request_body.get('password')

    # Validate email input
    if not is_valid_email(user_email):
        return generate_bad_request_response('Invalid Email address.')
    
    # Validate password input
    if not is_strong_password(user_password):
        return generate_bad_request_response('Password does not meet requirements.')

    # Check if user already exists
    user = queries.get_user_by_email(user_email)

    # User does not exist yet
    if not user:
        # Hash password with bcrypt and insert new user into database
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        user = queries.add_new_user(user_email, hashed_password.decode())

        return generate_auth_token_response(str(user.id), 'User created successfully.')
    
    # User already exists
    else:
        return generate_bad_request_response('User already exists. Please log in.')

@user.route('/login', methods = ['POST'])
def login():
    """
    Handles POST requests to /user/login 
        Parameters:
            -
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Parsing the request body
    request_body = request.get_json()
    user_email = request_body.get('email')
    user_password = request_body.get('password')
    
    # TODO: input validation

    # Check if user exists
    user = queries.get_user_by_email(user_email)

    # User does exist
    if user:
        password_check = bcrypt.checkpw(user_password.encode('utf-8'), user.password.encode('utf-8'))

        if user.email == user_email and password_check:
            return generate_auth_token_response(str(user.id), 'Login successful.')

    # User does not exist or password is wrong
    response_object = {
        'success': False,
        'message': 'Invalid email or password.'
    }
    return make_response(jsonify(response_object)), status.HTTP_401_UNAUTHORIZED

@user.route('/refresh', methods=['GET'])
@jwt_required
def refresh_session(user_id: str):
    """
    Handles GET requests to /user/refresh, used to refresh login sessions
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """
    
    # Generate a new jwt and return it, as session was already validated by jwt_required decorator
    return generate_auth_token_response(user_id, 'Session refreshed successfully.')