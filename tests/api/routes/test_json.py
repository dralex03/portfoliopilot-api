import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors
from tests.api.routes.helper_requests import register_user


def get_all_post_urls_with_json():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of all URL paths that use POST or PUT
                to test invalid JSON bodies.
    """
    return [
        ('POST', '/user/login', False),
        ('POST', '/user/register', False),
        # ('POST', '/user/portfolios/<portfolio_id>/add', True), # TODO
        ('POST', '/user/portfolios/create', True),
        # ('PUT', '/user/portfolios/<portfolio_id>/<p_element_id>', True), # TODO
        # ('PUT', '/user/portfolios/<portfolio_id>', True) # TODO
    ]

@pytest.mark.parametrize('method,path,login', get_all_post_urls_with_json())
def test_json_parsing(test_client: FlaskClient, method: str, path: str, login: bool):
    """
    Parametrized test to test all POST and PUT endpoints for correct behavior
    on invalid JSON bodies.
        Parameters:
            FlaskClient test_client;
            str method;
            str path;
            bool login;
        Returns:
            -
    """

    auth_token = None
    if login:
        auth_token = register_user(test_client, 'john.doe@example.com', 'Password123!')
    
    # Test invalid JSON body
    if method == 'POST':
        response = test_client.post(path,
                                    data='abc',
                                    content_type='application/json',
                                    headers={
                                        'Authorization': 'Bearer ' + auth_token
                                    } if auth_token else None
                                )

    elif method == 'PUT':
        response = test_client.put(path,
                                   data='abc',
                                   content_type='application/json',
                                   headers={
                                       'Authorization': 'Bearer ' + auth_token
                                   } if auth_token else None
                                )

    assert response.status_code == 500
    assert response.is_json

    assert not response.json['success']

    assert response.json['message'] == ApiErrors.invalid_json


    # Test invalid content type
    if method == 'POST':
        response = test_client.post(path,
                                    data={'foo': 'bar'},
                                    content_type='application/x-www-form-urlencoded',
                                    headers={
                                        'Authorization': 'Bearer ' + auth_token
                                    } if auth_token else None
                                )

    elif method == 'PUT':
        response = test_client.put(path,
                                   data={'foo': 'bar'},
                                   content_type='application/x-www-form-urlencoded',
                                   headers={
                                       'Authorization': 'Bearer ' + auth_token
                                   } if auth_token else None
                                )

    assert response.status_code == 400
    assert response.is_json

    assert not response.json['success']

    assert response.json['message'] == ApiErrors.body_is_not_json
