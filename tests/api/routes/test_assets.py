import pytest

from flask.testing import FlaskClient

from src.constants.errors import ApiErrors


def get_test_assets_info():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data.
    """
    return [
        ('AAPL', 'EQUITY', True, 200, ''),
        ('URTH', 'ETF', True, 200, ''),
        ('TEST123456', '', False, 404, ApiErrors.Assets.ticker_not_found)
    ]

@pytest.mark.parametrize('ticker,quote_type,valid,status_code,message', get_test_assets_info())
def test_get_asset_info(test_client: FlaskClient, ticker: str, quote_type: str, valid: bool, status_code: int, message: str):
    """
    Parametrized test to test the get asset info endpoint for correct behavior.
        Parameters:
            FlaskClient test_client;
            str ticker;
            str quote_type;
            bool valid;
            int status_code;
            str message;
        Returns:
            -
    """
    response = test_client.get(f'/assets/ticker/{ticker}')
    
    if valid:
        assert response.status_code == status_code
        assert response.is_json

        assert response.json['success']

        info = response.json['response']
        assert info['symbol'] == ticker
        assert info['quoteType'] == quote_type

        if quote_type == 'ETF':
            assert isinstance(info['navPrice'], float)
            assert info['etfData'] is not None
        
        if quote_type == 'EQUITY':
            assert isinstance(info['currentPrice'], float)
    else:
        assert response.status_code == status_code
        assert response.is_json

        assert not response.json['success']

        assert response.json['message'] == message


def get_test_search_assets():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data.
    """
    return [
        ('', None, ''),
        ('apple', None, 'AAPL'),
        ('apple', 'Germany', 'AAPL'),
        ('msci world etf', '', 'URTH'),
        ('verylongteststring123', '', ''),
    ]

@pytest.mark.parametrize('query,country,symbol', get_test_search_assets())
def test_search_assets(test_client: FlaskClient, query: str, country: str, symbol: str):
    """
    Parametrized test for search assets endpoint.
        Parameters:
            FlaskClient test_client;
            str query;
            str country;
            str symbol;
        Returns:
            -
    """
    response = test_client.get(f'/assets/search?query={query}&country={country}')

    # If no query was passed
    if query == '' or query is None:
        assert response.status_code == 400
        assert response.is_json
        assert not response.json['success']
        assert response.json['message'] == ApiErrors.missing_query_param('query')

        return
    
    assert response.status_code == 200
    assert response.is_json

    assert response.json['success']

    result = response.json['response']

    assert result['count'] == len(result['assets'])

    # Use symbol as indicator whether results are expected or not
    if symbol != '':
        assert result['count'] > 0

        assert len([
            a for a in result['assets']
                if a['symbol'] == symbol
        ]) >= 1
    else:
        assert result['count'] == 0



def get_test_asset_price_data():
    """
    Helper function that returns a list of test data.
        Parameters:
            -
        Returns:
            List[Tuple]: A list of test data.
    """
    return [
        ('AAPL', '1y', '1d', True, 200, ''),
        ('AAPL', '', '', False, 400, ApiErrors.missing_query_param('period')),
        ('AAPL', '1y', '', False, 400, ApiErrors.missing_query_param('interval')),
        ('AAPL', '1year', '1day', False, 400, ApiErrors.invalid_query_param('period')),
        ('AAPL', '1y', '1day', False, 400, ApiErrors.invalid_query_param('interval')),
        ('AAPL', '1y', '1m', False, 400, 'AAPL: 1m data not available for'),
        ('TESTTICKER123', '1y', '1d', False, 404, ApiErrors.Assets.ticker_not_found),
    ]

@pytest.mark.parametrize('ticker,period,interval,valid,status,message', get_test_asset_price_data())
def test_assets_price_data(
    test_client: FlaskClient, ticker: str, period: str, interval: str,
    valid: bool, status: int, message: str
    ):
    """
    Parametrized test for assets price data endpoint.
        Parameters:
            FlaskClient test_client;
            str ticker;
            str period;
            str interval;
            bool valid; 
            int status;
            str message;
        Returns:
            -
    """
    response = test_client.get(
        f'/assets/ticker/{ticker}/priceData?interval={interval}&period={period}'
        )
    
    assert response.status_code == status
    assert response.is_json

    # If no query was passed
    if valid:
        assert response.json['success']
        assert len(response.json['response']) > 0
    else:
        assert not response.json['success']
        assert message in response.json['message']
