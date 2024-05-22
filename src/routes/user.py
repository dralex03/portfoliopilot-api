import bcrypt
from flask import Blueprint, request, make_response, jsonify

from src.database import queries
from src.utils.input_validation import is_valid_email, is_strong_password
from src.utils import jwt_auth
from src.constants import http_status_codes as status

# Create blueprint which is used in the flask app
user = Blueprint('user', __name__)

@user.route('/register', methods = ['POST'])
def register():
    post_data = request.get_json()

    user_email = post_data.get('email')
    user_password = post_data.get('password')

    # Validate email and password inputs
    if not is_valid_email(user_email) or not is_strong_password(user_password):
        response_object = {
            'success': False,
            'message': 'Email or Password is invalid'
        }
        return make_response(jsonify(response_object)), status.HTTP_400_BAD_REQUEST

    # Check if user already exists
    user = queries.get_user_by_email(user_email)

    # User does not exist yet
    if not user:
        hashed_password = bcrypt.hashpw(user_password.encode('utf-8'), bcrypt.gensalt())
        user = queries.insert_new_user(user_email, hashed_password)

        auth_token = jwt_auth.encode_auth_token(user.id)

        if not auth_token:
            response_object = {
                'success': False,
                'message': 'Error creating Auth Token.'
            }
            return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR
        
        response_object = {
            'success': True,
            'message': 'User created successfully.',
            'auth_token': auth_token
        }
        return make_response(jsonify(response_object)), status.HTTP_201_CREATED
    
    # User already exists
    else:
        response_object = {
            'success': False,
            'message': 'User already exists. Please log in.'
        }
        return make_response(jsonify(response_object)), status.HTTP_400_BAD_REQUEST

@user.route('/login', methods = ['POST'])
def login():
    return 'Login2'