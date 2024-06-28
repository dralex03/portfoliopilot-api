from flask import Blueprint, request
from yfinance.exceptions import YFChartError

from src.utils.responses import *
from src.utils.request_parser import *
from src.constants.errors import ApiErrors
from src.constants.countries import COUNTRIES
from src.market_data.search import search_assets
from src.market_data.general_data import get_general_info
from src.market_data.price_data import get_price_data, VALID_INTERVALS, VALID_PERIODS
from src.market_data.etf_data import get_etf_info


# Create blueprint which is used in the flask app
assets = Blueprint('assets', __name__)


@assets.route('/search', methods=['GET'])
def search_assets():
    """
    Handles GET requests to /assets/search, used to search assets.
        Parameters:
            -
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    query = request.args.get('query')
    country = request.args.get('country')

    # "query" is a required parameter
    if not isinstance(query, str) or len(query) <= 0:
        return generate_bad_request_response(ApiErrors.missing_query_param('query'))
    
    # "country" is optional, but needs to be valid
    # if its not valid, we default it to None
    if isinstance(country, str) and len(country) > 0:
        if country.lower() not in COUNTRIES:
            country = None
    else:
        country = None

    return generate_success_response(search_assets(query, country))


@assets.route('/ticker/<ticker>', methods=['GET'])
def ticker_info(ticker: str):
    """
    Handles GET requests to /assets/ticker/<ticker>, used to get information
    about a specific ticker.
        Parameters:
            str ticker;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # "ticker" is a required parameter
    if len(ticker) <= 0:
        return generate_bad_request_response(
            ApiErrors.Assets.ticker_info_missing_ticker
            )
    
    asset_info = get_general_info(ticker)

    # Check if asset with this ticker exists
    if asset_info is None:
        return generate_not_found_response(ApiErrors.Assets.ticker_not_found)
    
    # Add extra data for ETFs
    if asset_info.get('quoteType') == 'ETF':
        asset_info['etf_data'] = get_etf_info(ticker)

    return generate_success_response(asset_info)


@assets.route('/ticker/<ticker>/priceData', methods=['GET'])
def ticker_price_data(ticker: str):
    """
    Handles GET requests to /assets/ticker/<ticker>/priceData,
    used to get information about a specific ticker.
        Parameters:
            str ticker;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # "ticker" is a required parameter
    if len(ticker) <= 0:
        return generate_bad_request_response(
            ApiErrors.Assets.ticker_info_missing_ticker
            )
    
    period = request.args.get('period')
    interval = request.args.get('interval')

    # "period" and "interval" are required
    if not isinstance(period, str) or len(period) <= 0:
        return generate_bad_request_response(
            ApiErrors.missing_query_param('period')
            )
    if not isinstance(interval, str) or len(interval) <= 0:
        return generate_bad_request_response(
            ApiErrors.missing_query_param('interval')
            )
    
    period = period.lower()
    interval = interval.lower()
    
    # Validating period and interval for valid values
    if period not in VALID_PERIODS:
        return generate_bad_request_response(
            ApiErrors.invalid_query_param('period')
            )
    if interval not in VALID_INTERVALS:
        return generate_bad_request_response(
            ApiErrors.invalid_query_param('interval')
            )
    
    try:
        price_data = get_price_data(ticker, period, interval)
    except YFChartError as e: # invalid interval for requested period
        return generate_bad_request_response(str(e))
    except Exception as e:
        return generate_internal_error_response(
            ApiErrors.Assets.ticker_price_data_error, e
            )

    # Check if asset with this ticker exists
    if price_data is None:
        return generate_not_found_response(ApiErrors.Assets.ticker_not_found)

    return generate_success_response(price_data)