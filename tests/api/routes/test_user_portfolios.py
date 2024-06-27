import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors
from src.constants.messages import ApiMessages

from tests.api.routes.helper_requests import login_user, create_portfolio



def get_test_portfolios_create():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing.
    """
    return [
        ('Portfolio123', True, 200, ''),
        ('Portfolio123', False, 400, ApiErrors.Portfolio.portfolio_already_exists),
        ('', False, 400, ApiErrors.field_is_empty('name')),
        (None, False, 400, ApiErrors.field_wrong_type('name', 'string')),
    ]

@pytest.mark.parametrize('portfolio_name,valid,status_code,message', get_test_portfolios_create())
def test_create_user_portfolio(test_client: FlaskClient, 
                               portfolio_name: str,
                               valid: bool,
                               status_code: int,
                               message: str):
    """
    Parametrized test to the create portfolio endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str portfolio_name;
            bool valid
            int status_code;
            str message;
        Returns:
            -
    """

    auth_token = login_user(test_client, 'john.doe@example.com', 'Password123!')
    assert auth_token is not None

    response = test_client.post('/user/portfolios/create',
                                json={
                                    'name': portfolio_name
                                },
                                headers={
                                    'Authorization': 'Bearer ' + auth_token
                                })

    assert response.status_code == status_code
    assert response.is_json

    if valid:
        assert response.json['success']
        assert 'id' in response.json['response']
    else:
        assert not response.json['success']
        assert response.json['message'] == message



def get_test_portfolios():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing.
    """
    return [
        ('Portfolio123', 1),
        ('PortfolioTest', 2),
    ]


@pytest.mark.parametrize('portfolio_name,count', get_test_portfolios())
def test_get_all_user_portfolios_no_elements(test_client: FlaskClient,
                                             portfolio_name: str,
                                             count: int):
    """
    Parametrized test to the get portfolios endpoint for correct behavior
    with empty portfolios.
        Parameters:
            FlaskClient test_client;
            str portfolio_name;
            int count;
        Returns:
            -
    """

    auth_token = login_user(test_client, 'jane.doe@example2.com', 'Password123!')
    assert auth_token is not None

    portfolio_id = create_portfolio(test_client, auth_token, portfolio_name)
    assert portfolio_id is not None

    response = test_client.get('/user/portfolios',
                               headers={
                                   'Authorization': 'Bearer ' + auth_token
                               })

    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']
    assert len(response.json['response']) == count
    assert response.json['response'][count-1]['id'] == portfolio_id


def test_get_all_user_portfolios_empty(test_client: FlaskClient):
    """
    Test to the get portfolios endpoint for correct behavior
    without any portfolios.
        Parameters:
            FlaskClient test_client;
        Returns:
            -
    """

    auth_token = login_user(test_client, 'james.brown@example.com', 'Password123!')
    assert auth_token is not None

    response = test_client.get('/user/portfolios',
                               headers={
                                   'Authorization': 'Bearer ' + auth_token
                               })

    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']
    assert len(response.json['response']) == 0


@pytest.mark.parametrize('portfolio_name,_', get_test_portfolios())
def test_get_user_portfolio_and_delete(test_client: FlaskClient, portfolio_name: str, _):
    """
    Parametrized test to the get portfolio and delete portfolio endpoints
    for correct behavior.
        Parameters:
            FlaskClient test_client;
            str portfolio_name;
        Returns:
            -
    """
    auth_token = login_user(test_client, 'alex@example.com', 'Password123!')
    assert auth_token is not None

    portfolio_id = create_portfolio(test_client, auth_token, portfolio_name)
    assert portfolio_id is not None

    response = test_client.get(f'/user/portfolios/{portfolio_id}',
                               headers={
                                   'Authorization': 'Bearer ' + auth_token
                               })

    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']
    assert 'id' in response.json['response'] and response.json['response']['id'] == portfolio_id

    # Testing deletion
    response = test_client.delete(f'/user/portfolios/{portfolio_id}',
                                  headers={
                                      'Authorization': 'Bearer ' + auth_token
                                  })

    assert response.status_code == 200
    assert response.is_json
    assert response.json['success']
    assert response.json['response'] == ApiMessages.delete_data_by_id_success('portfolio', portfolio_id)

    # Testing deletion for already deleted portfolios
    response = test_client.delete(f'/user/portfolios/{portfolio_id}',
                                  headers={
                                      'Authorization': 'Bearer ' + auth_token
                                  })

    assert response.status_code == 404
    assert response.is_json
    assert not response.json['success']
    assert response.json['message'] == ApiErrors.data_by_id_not_found('portfolio', portfolio_id)


"""
TODO: below are tests that need to be fixed
"""

# @pytest.mark.parametrize("user_id,portfolio_id", [('user123', 'portfolio1'), ('user456', 'portfolio2')])
# def test_update_user_portfolio(test_client: FlaskClient, user_id: str, portfolio_id: str):
#     auth_token = login_user(test_client, user_id, 'Password!')
#     assert auth_token is not None

#     response = test_client.put(f'/user/portfolios/{portfolio_id}',
#                                json={
#                                    'name': 'Updated Portfolio Name'
#                                },
#                                headers={
#                                    'Authorization': 'Bearer ' + auth_token
#                                })

#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['success']
#     assert response.json['response']['name'] == 'Updated Portfolio Name'

# @pytest.mark.parametrize("user_id,portfolio_id", [('user123', 'portfolio1'), ('user456', 'portfolio2')])
# def test_add_element_to_user_portfolio(test_client: FlaskClient, user_id: str, portfolio_id: str):
#     auth_token = login_user(test_client, user_id, 'Password!')
#     assert auth_token is not None

#     p_element_id = add_portfolio_element(test_client, portfolio_id, 'AAPL', 10, 150.00, 2.50, auth_token)
#     assert p_element_id is not None

#     response = test_client.post(f'/user/portfolios/{portfolio_id}/add',
#                                 json={
#                                     'asset_ticker': 'AAPL',
#                                     'count': 10,
#                                     'buy_price': 150.00,
#                                     'order_fee': 2.50
#                                 },
#                                 headers={
#                                     'Authorization': 'Bearer ' + auth_token
#                                 })

#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['success']
#     assert 'id' in response.json['response']

# @pytest.mark.parametrize("user_id,portfolio_id,p_element_id", [('user123', 'portfolio1', 'elem1'), ('user456', 'portfolio2', 'elem2')])
# def test_get_element_of_user_portfolio(test_client: FlaskClient, user_id: str, portfolio_id: str, p_element_id: str):
#     auth_token = login_user(test_client, user_id, 'Password!')
#     assert auth_token is not None

#     response = test_client.get(f'/user/portfolios/{portfolio_id}/{p_element_id}',
#                                headers={
#                                    'Authorization': 'Bearer ' + auth_token
#                                })

#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['success']
#     assert response.json['response']['id'] == p_element_id

# @pytest.mark.parametrize("user_id,portfolio_id,p_element_id", [('user123', 'portfolio1', 'elem1'), ('user456', 'portfolio2', 'elem2')])
# def test_delete_element_from_user_portfolio(test_client: FlaskClient, user_id: str, portfolio_id: str, p_element_id: str):
#     auth_token = login_user(test_client, user_id, 'Password!')
#     assert auth_token is not None

#     response = test_client.delete(f'/user/portfolios/{portfolio_id}/{p_element_id}',
#                                   headers={
#                                       'Authorization': 'Bearer ' + auth_token
#                                   })

#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['success']
#     assert response.json['response']['message'] == ApiMessages.delete_data_by_id_success('portfolio element', p_element_id)

# @pytest.mark.parametrize("user_id,portfolio_id,p_element_id", [('user123', 'portfolio1', 'elem1'), ('user456', 'portfolio2', 'elem2')])
# def test_update_element_of_user_portfolio(test_client: FlaskClient, user_id: str, portfolio_id: str, p_element_id: str):
#     auth_token = login_user(test_client, user_id, 'Password!')
#     assert auth_token is not None

#     response = test_client.put(f'/user/portfolios/{portfolio_id}/{p_element_id}',
#                                json={
#                                    'count': 20,
#                                    'buy_price': 155.00,
#                                    'order_fee': 3.00
#                                },
#                                headers={
#                                    'Authorization': 'Bearer ' + auth_token
#                                })

#     assert response.status_code == 200
#     assert response.is_json
#     assert response.json['success']
#     assert response.json['response']['id'] == p_element_id
