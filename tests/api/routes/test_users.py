import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors
from src.constants.messages import ApiMessages

from tests.api.routes.helper_requests import login_user


def get_test_users_register():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing user registration request.
    """
    return [
        # Valid Test Cases
        ('john.doe@example.com', 'Password123!', True, 200, ApiMessages.User.register_success),
        ('jane.smith@example.com', 'Abcdef1!', True, 200, ApiMessages.User.register_success),
        
        # User already exists Test Case
        ('jane.smith@example.com', 'Abcdefgh1@', False, 400, ApiErrors.User.register_already_exists),

        # Invalid user input Test Cases
        ('john.doe@example.com', 'Password', False, 400, ApiErrors.User.register_invalid_password),
        ('john.doe@example.com', 'password123!', False, 400, ApiErrors.User.register_invalid_password),
        ('john.doe@example.com', 'PASSWORD123!', False, 400, ApiErrors.User.register_invalid_password),
        ('john.doe@example.com', 'Password123', False, 400, ApiErrors.User.register_invalid_password),
        ('jane.smith@example.com', '123456789!', False, 400, ApiErrors.User.register_invalid_password),
        ('jane.smith@example.com', '', False, 400, ApiErrors.User.register_invalid_password),
        ('jane.smith@example', 'Password123!', False, 400, ApiErrors.User.register_invalid_email),
        ('jane.smith@', 'Password123!', False, 400, ApiErrors.User.register_invalid_email),
        ('jane.smith@', 'Password!', False, 400, ApiErrors.User.register_invalid_email),
        ('@example.com', 'Password123!', False, 400, ApiErrors.User.register_invalid_email),

        # Invalid request inputs Test Cases
        (None, None, False, 400, ApiErrors.field_wrong_type('email', 'string')),
        ('john.doe@example.com', None, False, 400, ApiErrors.field_wrong_type('password', 'string')),
        (None, 'password123!', False, 400, ApiErrors.field_wrong_type('email', 'string')),
    ]

@pytest.mark.parametrize('email,password,valid,status_code,message', get_test_users_register())
def test_user_registration(test_client: FlaskClient, email: str, password: str, valid: bool, status_code: int, message: str):
    """
    Parametrized test to the user registration endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str email;
            str password;
            bool valid;
            int status_code;
            str password;
        Returns:
            -
    """
    response = test_client.post('/user/register',
                                json={
                                    'email': email,
                                    'password': password
                                })
    
    if valid:
        assert response.status_code == status_code
        assert response.is_json

        assert response.json['success']

        assert response.json['response']['message'] == message
        assert response.json['response']['auth_token'] is not None
    else:
        assert response.status_code == status_code
        assert response.is_json

        assert not response.json['success']

        assert response.json['message'] == message



def get_test_users_login():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing user login request.
    """
    return [
        # Valid Test Cases
        ('john.doe@example.com', 'Password123!', True, 200, ApiMessages.User.login_success),
        ('jane.smith@example.com', 'Abcdef1!', True, 200, ApiMessages.User.login_success),
        
        # Invalid Credentials Test Cases
        ('jane.smith@example.com', 'Abcdefgh1@', False, 401, ApiErrors.User.login_invalid_credentials),
        ('john.doe@example.com', 'Password!', False, 401, ApiErrors.User.login_invalid_credentials),
        ('john@example.com', 'Password!', False, 401, ApiErrors.User.login_invalid_credentials),

        # Invalid request inputs Test Cases
        (None, None, False, 400, ApiErrors.field_wrong_type('email', 'string')),
        ('john.doe@example.com', None, False, 400, ApiErrors.field_wrong_type('password', 'string')),
        (None, 'password123!', False, 400, ApiErrors.field_wrong_type('email', 'string')),
    ]

@pytest.mark.parametrize('email,password,valid,status_code,message', get_test_users_login())
def test_user_login(test_client: FlaskClient, email: str, password: str, valid: bool, status_code: int, message: str):
    """
    Parametrized test to the user login endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str email;
            str password;
            bool valid;
            int status_code;
            str password;
        Returns:
            -
    """

    response = test_client.post('/user/login',
                                json={
                                    'email': email,
                                    'password': password
                                })
    
    if valid:
        assert response.status_code == status_code
        assert response.is_json

        assert response.json['success']

        assert response.json['response']['message'] == message

        assert response.json['response']['auth_token'] is not None
    else:
        assert response.status_code == status_code
        assert response.is_json

        assert not response.json['success']

        assert response.json['message'] == message


def get_test_users_refresh_session():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing user
                session refresh request.
    """
    return [
        # Valid Test Cases
        ('john.doe@example.com', 'Password123!'),
        ('jane.smith@example.com', 'Abcdef1!')
    ]

@pytest.mark.parametrize("email,password", get_test_users_refresh_session())
def test_user_refresh(test_client: FlaskClient, email: str, password: str):
    """
    Parametrized test to the user refresh endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str email;
            str password;
        Returns:
            -
    """
    auth_token = login_user(test_client, email, password)
    assert auth_token is not None

    response = test_client.get('/user/refresh',
                                headers={
                                    'Authorization': 'Bearer ' + auth_token
                                })
    
    assert response.status_code == 200
    assert response.is_json

    assert response.json['success']

    assert response.json['response']['message'] == ApiMessages.User.session_refresh_success
    assert response.json['response']['auth_token'] is not None
