import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors
from tests.api.conftest import test_client
from tests.api.routes.helper_requests import login_user


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
        ('POST', '/user/login'),
        ('POST', '/user/register')
        # ('POST', '/user/portfolios/<portfolio_id>/add'), # TODO: requires jwt auth
        # ('POST', '/user/portfolios/create'), # TODO: requires jwt auth
        # ('PUT', '/user/portfolios/<portfolio_id>/<p_element_id>'), # TODO: requires jwt auth
        # ('PUT', '/user/portfolios/<portfolio_id>'), # TODO: requires jwt auth
    ]

@pytest.mark.parametrize("method, path", get_all_post_urls_with_json())
def test_json_parsing(test_client: FlaskClient, method: str, path: str):
    """
    Parametrized test to test all POST and PUT endpoints for correct behavior
    on invalid JSON bodies.
        Parameters:
            FlaskClient test_client;
            str method;
            str path;
        Returns:
            -
    """
    
    # Test invalid JSON body
    if method == 'POST':
        response = test_client.post(path, data='abc', content_type='application/json')
    elif method == 'PUT':
        response = test_client.put(path, data='abc', content_type='application/json')

    assert response.status_code == 500
    assert response.is_json

    assert not response.json['success']

    assert response.json['message'] == ApiErrors.invalid_json


    # Test invalid content type
    if method == 'POST':
        response = test_client.post(path, data={'foo': 'bar'}, content_type='application/x-www-form-urlencoded')
    elif method == 'PUT':
        response = test_client.put(path, data={'foo': 'bar'}, content_type='application/x-www-form-urlencoded')

    assert response.status_code == 400
    assert response.is_json

    assert not response.json['success']

    assert response.json['message'] == ApiErrors.body_is_not_json
