from flask import Blueprint, request
from sqlalchemy.exc import IntegrityError

from src.database import queries, models
from src.utils.decorators import jwt_required, validate_portfolio_owner
from src.utils.responses import *
from src.utils.request_parser import parse_json_request_body
from src.constants.errors import ApiErrors
from src.constants.messages import ApiMessages
from src.market_data.general_data import get_general_info
from src.constants.asset_types import QUOTE_TYPE_LIST

# Create blueprint which is used in the flask app
user_portfolios = Blueprint('portfolio', __name__)


@user_portfolios.route('', methods = ['GET'])
@jwt_required
def get_all_user_portfolios(user_id: str):
    """
    Handles GET requests to /user/portfolios
    Returns all portfolios of the user including all elements as a list.
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    try:
        portfolios: list[models.Portfolio] = queries.get_portfolios_by_user_id(user_id)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.get_portfolios_by_user_id_error, e)

    return generate_success_response([p.to_json() for p in portfolios])


@user_portfolios.route('/<portfolio_id>', methods = ['GET'])
@jwt_required
@validate_portfolio_owner
def get_user_portfolio(user_id: str, portfolio: models.Portfolio):
    """
    Handles GET requests to /user/portfolios/<portfolio_id> where <portfolio_id> is the ID of a users portfolio.
    Returns the portfolio with all elements as response.
        Parameters:
            str user_id;
            Portfolio portfolio;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    return generate_success_response(portfolio.to_json())


@user_portfolios.route('/<portfolio_id>', methods = ['DELETE'])
@jwt_required
@validate_portfolio_owner
def delete_user_portfolio(user_id: str, portfolio: models.Portfolio):
    """
    Handles DELETE requests to /user/portfolios/<portfolio_id> where <portfolio_id> is the ID of a users portfolio.
    Deletes the portfolio.
        Parameters:
            str user_id;
            Portfolio portfolio;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Try to delete portfolio
    try:
        portfolio_deleted = queries.delete_portfolio_by_id(portfolio.id)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.delete_data_by_id_error('portfolio', portfolio.id), e)
    
    # Check if portfolio was deleted successfully
    if portfolio_deleted == True:
        return generate_success_response(ApiMessages.delete_data_by_id_success('portfolio', portfolio.id))
    else: 
        # Will only be reached in rare edge cases as the
        # "validate_portfolio_owner" decorator handles this case already.
        message = ApiErrors.data_by_id_not_found('portfolio', portfolio.id)
        return generate_not_found_response(message)


@user_portfolios.route('/create', methods = ['POST'])
@jwt_required
def create_user_portfolio(user_id: str):
    """
    Handles POST requests to /user/portfolios/create.
    Used to create a new portfolio.
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Parsing the Request Body
    try:
        request_body = parse_json_request_body(request)
    except ValueError as e:
        return generate_bad_request_response(str(e))
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.invalid_json, e)
    
    portfolio_name = request_body.get('name')

    # Validating field types
    if not isinstance(portfolio_name, str):
        return generate_bad_request_response(ApiErrors.field_wrong_type('name', 'string'))

    # Validating field values
    if not len(portfolio_name) > 0:
        return generate_bad_request_response(ApiErrors.field_is_empty('name'))

    try:
        portfolio: models.Portfolio = queries.add_portfolio(portfolio_name, user_id)
    except IntegrityError as e:
        return generate_bad_request_response(ApiErrors.Portfolio.portfolio_already_exists)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.add_portfolio_error, e)

    return generate_success_response(portfolio.to_json())


@user_portfolios.route('/<portfolio_id>', methods = ['PUT'])
@jwt_required
@validate_portfolio_owner
def update_user_portfolio(user_id: str, portfolio: models.Portfolio):
    """
    Handles PUT requests to /user/portfolios/<portfolio_id> where <portfolio_id> is the ID of a users portfolio.
    Used to update the portfolio, for example the name.
        Parameters:
            str user_id;
            Portfolio portfolio;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """
    
    # Parsing the request body
    try:
        request_body = parse_json_request_body(request)
    except ValueError as e:
        return generate_bad_request_response(str(e))
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.invalid_json, e)
    
    portfolio_name = request_body.get('name')
    
    # Validating field types
    if not isinstance(portfolio_name, str):
        return generate_bad_request_response(ApiErrors.field_wrong_type('name', 'string'))

    # Validating field values
    if not len(portfolio_name) > 0:
        return generate_bad_request_response(ApiErrors.field_is_empty('name'))

    # Checking if user already owns a portfolio with this name
    try:
        existing_portfolio = queries.get_portfolio_by_name(user_id, portfolio_name)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.update_portfolio_name_error, e)
    
    if existing_portfolio is not None:
        return generate_bad_request_response(ApiErrors.Portfolio.portfolio_already_exists)


    # Updating Portfolio Name and sending updated portfolio in response
    try:
        portfolio: models.Portfolio = queries.update_portfolio_name(portfolio.id, portfolio_name)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.update_portfolio_name_error, e)

    return generate_success_response(portfolio.to_json())


@user_portfolios.route('/<portfolio_id>/add', methods = ['POST'])
@jwt_required
@validate_portfolio_owner
def add_element_to_user_portfolio(user_id: str, portfolio: models.Portfolio):
    """
    Handles POST requests to /user/portfolios/<portfolio_id>/add where <portfolio_id> is the ID of a users portfolio.
    Creates a new portfolio element in the portfolio.
        Parameters:
            str user_id;
            Portfolio portfolio;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Parsing the request body
    try:
        request_body = parse_json_request_body(request)
    except ValueError as e:
        return generate_bad_request_response(str(e))
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.invalid_json, e)
    
    
    asset_ticker = request_body.get('asset_ticker')
    count = request_body.get('count')
    buy_price = request_body.get('buy_price')
    order_fee = request_body.get('order_fee')

    # Convert ints to floats
    if isinstance(count, int):
        count = float(count)
    if isinstance(buy_price, int):
        buy_price = float(buy_price)
    if isinstance(order_fee, int):
        order_fee = float(order_fee)

    # Validating field types
    if not isinstance(asset_ticker, str):
        return generate_bad_request_response(ApiErrors.field_wrong_type('asset_ticker', 'string'))
    if not isinstance(count, float):
        return generate_bad_request_response(ApiErrors.field_wrong_type('count', 'float'))
    if not isinstance(buy_price, float):
        return generate_bad_request_response(ApiErrors.field_wrong_type('buy_price', 'float'))
    if not isinstance(order_fee, float):
        return generate_bad_request_response(ApiErrors.field_wrong_type('order_fee', 'float'))
    
    # Validating field values
    if not len(asset_ticker) > 0:
        return generate_bad_request_response(ApiErrors.field_is_empty('asset_ticker'))
    if not count > 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('count', '0', '>'))
    if not buy_price > 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('buy_price', '0', '>'))
    if not order_fee >= 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('order_fee', '0', '>='))
    
    # Check if the asset already exists
    try:
        asset: models.Asset = queries.get_asset_by_ticker(asset_ticker)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.get_asset_by_ticker_error, e)


    # Add asset if its not in database yet
    if asset is None:
        asset_info = get_general_info(asset_ticker)

        # Check if asset with this ticker exists
        if asset_info is None:
            return generate_bad_request_response(
                ApiErrors.Portfolio.portfolio_element_asset_invalid_ticker
            )

        asset_quote_type = asset_info.get('quoteType')

        # Make sure the asset type is supported
        if not asset_quote_type in QUOTE_TYPE_LIST:
            return generate_bad_request_response(
                ApiErrors.Portfolio.portfolio_element_asset_invalid_type
            )
        
        # Find correct asset type id
        try:
            asset_type: models.AssetType = queries.get_asset_type_by_quote_type(asset_quote_type)
        except Exception as e: # pragma: no cover
            return generate_internal_error_response(
                ApiErrors.Portfolio.add_portfolio_element_error, e
            )
        
        # Add new asset to database
        try:
            asset = queries.add_new_asset(
                asset_info.get('shortName', asset_ticker),
                asset_ticker,
                asset_info.get('isin'),
                asset_info.get('currency'),
                asset_type.id
            )
        except Exception as e: # pragma: no cover
            return generate_internal_error_response(
                ApiErrors.Portfolio.add_portfolio_element_error, e
            )


    # Trying to add the element to the portfolio
    try:
        portfolio_element: models.PortfolioElement = queries.add_portfolio_element(
            portfolio.id, asset.id, count, buy_price, order_fee
        )
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(
            ApiErrors.Portfolio.add_portfolio_element_error, e
        )
    
    return generate_success_response(portfolio_element.to_json())


@user_portfolios.route('/<portfolio_id>/<p_element_id>', methods = ['GET'])
@jwt_required
@validate_portfolio_owner
def get_element_of_user_portfolio(user_id: str, portfolio: models.Portfolio, p_element_id: str):
    """
    Handles GET requests to /user/portfolios/<portfolio_id>/<p_element_id> where
    <portfolio_id> is the ID of a users portfolio and
    <p_element_id> is the ID of a portfolio element (asset) in that portfolio.
    Returns the portfolio element as Response.
        Parameters:
            str user_id;
            Portfolio portfolio;
            str p_element_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """
    
    # Trying to fetch the portfolio element
    try:
        portfolio_element: models.PortfolioElement = queries.get_portfolio_element(portfolio.id, p_element_id)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.get_portfolio_element_error, e)
    
    return generate_success_response(portfolio_element.to_json())


@user_portfolios.route('/<portfolio_id>/<p_element_id>', methods = ['DELETE'])
@jwt_required
@validate_portfolio_owner
def delete_element_from_user_portfolio(user_id: str, portfolio: models.Portfolio, p_element_id: str):
    """
    Handles DELETE requests to /user/portfolios/<portfolio_id>/<p_element_id> where
    <portfolio_id> is the ID of a users portfolio and
    <p_element_id> is the ID of a portfolio element (asset) in that portfolio.
    Deletes the portfolio element.
        Parameters:
            str user_id;
            Portfolio portfolio;
            str p_element_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """
    
    # Trying to delete the portfolio element
    try:
        element_deleted: models.PortfolioElement = queries.delete_portfolio_element(portfolio.id, p_element_id)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.delete_data_by_id_error('portfolio element', p_element_id), e)
    
    # Check if portfolio was deleted successfully
    if element_deleted == True:
        return generate_success_response(ApiMessages.delete_data_by_id_success('portfolio element', p_element_id))
    else:
        message = ApiErrors.data_by_id_not_found('portfolio element',
                                                 p_element_id)
        return generate_not_found_response(message)


@user_portfolios.route('/<portfolio_id>/<p_element_id>', methods = ['PUT'])
@jwt_required
@validate_portfolio_owner
def update_element_of_user_portfolio(user_id: str, portfolio: models.Portfolio, p_element_id: str):
    """
    Handles PUT requests to /user/portfolios/<portfolio_id>/<p_element_id> where
    <portfolio_id> is the ID of a users portfolio and
    <p_element_id> is the ID of a portfolio element (asset) in that portfolio.
    Used to update details of a specific portfolio element, for example the count.
        Parameters:
            str user_id;
            Portfolio portfolio;
            str p_element_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    # Parsing the request body
    try:
        request_body = parse_json_request_body(request)
    except ValueError as e:
        return generate_bad_request_response(str(e))
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.invalid_json, e)
    
    
    count = request_body.get('count', None)
    buy_price = request_body.get('buy_price', None)
    order_fee = request_body.get('order_fee', None)

    # Convert ints to floats
    if isinstance(count, int):
        count = float(count)
    if isinstance(buy_price, int):
        buy_price = float(buy_price)
    if isinstance(order_fee, int):
        order_fee = float(order_fee)


    # Validating field types
    if not isinstance(count, float) and count is not None:
        return generate_bad_request_response(ApiErrors.field_wrong_type('count', 'float'))
    if not isinstance(buy_price, float) and buy_price is not None:
        return generate_bad_request_response(ApiErrors.field_wrong_type('buy_price', 'float'))
    if not isinstance(order_fee, float) and order_fee is not None:
        return generate_bad_request_response(ApiErrors.field_wrong_type('order_fee', 'float'))
    
    # Check for at least one value thats not None
    if count is None and buy_price is None and order_fee is None:
        return generate_bad_request_response(ApiErrors.Portfolio.update_p_element_all_values_none)
    
    # Validating field values
    if not count > 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('count', '0', '>'))
    if not buy_price > 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('buy_price', '0', '>'))
    if not order_fee >= 0:
        return generate_bad_request_response(ApiErrors.num_field_out_of_limit('order_fee', '0', '>='))
    
    # Trying to update the portfolio element
    try:
        portfolio_element: models.PortfolioElement = queries.update_portfolio_element(portfolio.id, p_element_id, count, buy_price, order_fee)
    except Exception as e: # pragma: no cover
        return generate_internal_error_response(ApiErrors.Portfolio.update_portfolio_element_error, e)
    
    # Check if the portfolio element was deleted because the count was 0 or less
    if portfolio_element == 'deleted':
        return generate_success_response(ApiMessages.Portfolio.p_element_deleted_cause_count_zero(p_element_id))
    
    return generate_success_response(portfolio_element.to_json())