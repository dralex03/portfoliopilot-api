import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors
from src.constants.messages import ApiMessages

from tests.api.routes.helper_requests import (
    login_user, create_portfolio, get_portfolio
)



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



def get_test_portfolios_update():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing.
    """
    return [
        ('Portfolio123', 'Portfolio1', True, 200, ''),
        ('Test123', 'Portfolio1', False, 400, ApiErrors.Portfolio.portfolio_already_exists),
        ('Test1', '', False, 400, ApiErrors.field_is_empty('name')),
        ('Test2', None, False, 400, ApiErrors.field_wrong_type('name', 'string')),
    ]

@pytest.mark.parametrize('p_name,name_new,valid,status_code,message', get_test_portfolios_update())
def test_update_user_portfolio(test_client: FlaskClient, 
                               p_name: str,
                               name_new: str,
                               valid: bool,
                               status_code: int,
                               message: str):
    """
    Parametrized test to the update portfolio endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str p_name;
            str name_new;
            bool valid
            int status_code;
            str message;
        Returns:
            -
    """

    auth_token = login_user(test_client, 'bob@example.com', 'Password123!')
    assert auth_token is not None

    portfolio_id = create_portfolio(test_client, auth_token, p_name)
    assert portfolio_id is not None

    
    response = test_client.put(f'/user/portfolios/{portfolio_id}',
                                  json={
                                      'name': name_new
                                  },
                                  headers={
                                      'Authorization': 'Bearer ' + auth_token
                                  })

    assert response.status_code == status_code
    assert response.is_json

    if valid:
        assert response.json['success']

        assert 'id' in response.json['response']
        assert response.json['response']['id'] == portfolio_id

        assert 'name' in response.json['response']
        assert response.json['response']['name'] == name_new
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



def get_test_add_portfolio_element():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data for testing.
    """
    return [
        ('AAPL', 10.0, 150.0, 3.46, True, 200, ''),
        ('NVDA', 10, 100, 3, True, 200, ''),
        
        (None, 10.0, 150.0, 3.46, False, 400, ApiErrors.field_wrong_type('asset_ticker', 'string')),
        ('AAPL', '10.0', 150.0, 3.46, False, 400, ApiErrors.field_wrong_type('count', 'float')),
        ('AAPL', 10.0, '150.0', 3.46, False, 400, ApiErrors.field_wrong_type('buy_price', 'float')),
        ('AAPL', 10.0, 150.0, '3.46', False, 400, ApiErrors.field_wrong_type('order_fee', 'float')),

        ('', 10.0, 150.0, 3.46, False, 400, ApiErrors.field_is_empty('asset_ticker')),
        ('AAPL', 0, 150.0, 3.46, False, 400, ApiErrors.num_field_out_of_limit('count', '0', '>')),
        ('AAPL', 10.0, 0, 3.46, False, 400, ApiErrors.num_field_out_of_limit('buy_price', '0', '>')),
        ('AAPL', 10.0, 150.0, -1, False, 400, ApiErrors.num_field_out_of_limit('order_fee', '0', '>=')),

        ('INVALID_TICKER', 10.0, 150.0, 3.46, False, 400, ApiErrors.Portfolio.portfolio_element_asset_invalid_ticker),

        ('EURUSD=X', 10.0, 150.0, 3.46, False, 400, ApiErrors.Portfolio.portfolio_element_asset_invalid_type),
    ]

@pytest.mark.parametrize('ticker,count,buy_price,order_fee,valid,status_code,message', get_test_add_portfolio_element())
def test_add_portfolio_element(test_client: FlaskClient, 
                               ticker: str,
                               count: float,
                               buy_price: float,
                               order_fee: float,
                               valid: bool,
                               status_code: int,
                               message: str):
    """
    Parametrized test to the update portfolio endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str ticker;
            float count;
            float buy_price;
            float order_fee;
            bool valid
            int status_code;
            str message;
        Returns:
            -
    """

    auth_token = login_user(test_client, 'fred@example.com', 'Password123!')
    assert auth_token is not None

    portfolio_id = get_portfolio(test_client, auth_token, 'Portfolio123')
    assert portfolio_id is not None

    
    response = test_client.post(f'/user/portfolios/{portfolio_id}/add',
                                  json={
                                      'asset_ticker': ticker,
                                      'count': count,
                                      'buy_price': buy_price,
                                      'order_fee': order_fee
                                  },
                                  headers={
                                      'Authorization': 'Bearer ' + auth_token
                                  })

    print(response.get_json())
    assert response.status_code == status_code
    assert response.is_json

    if valid:
        assert response.json['success']

        assert 'id' in response.json['response']
        assert 'portfolio_id' in response.json['response']
        assert response.json['response']['portfolio_id'] == portfolio_id

        
        assert 'count' in response.json['response']
        assert response.json['response']['count'] == float(count)
        assert 'buy_price' in response.json['response']
        assert response.json['response']['buy_price'] == float(buy_price)
        assert 'order_fee' in response.json['response']
        assert response.json['response']['order_fee'] == float(order_fee)

        assert 'asset' in response.json['response']

        asset = response.json['response']['asset']
        
        assert 'name' in asset
        assert 'default_currency' in asset
        assert 'asset_type' in asset

        assert 'ticker_symbol' in asset
        assert asset['ticker_symbol'] == ticker
    else:
        assert not response.json['success']
        assert response.json['message'] == message
