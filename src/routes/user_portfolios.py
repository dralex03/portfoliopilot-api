from flask import Blueprint, request, make_response, jsonify
from sqlalchemy.exc import IntegrityError

from src.constants import http_status_codes as status
from src.database import queries, models
from src.utils.decorators import jwt_required, validate_portfolio_owner
from src.utils.responses import *

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
        portfolios: list[models.Portfolio] = queries.get_portfolio_by_user_id(user_id)
    except Exception as e:
        return generate_internal_error_response('Error fetching all portfolios.', e)

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
    except Exception as e:
        return generate_internal_error_response(f'Error deleting portfolio with ID "{portfolio.id}".', e)
    
    # Check if portfolio was deleted successfully
    if portfolio_deleted == True:
        return generate_success_response(f'Portfolio with ID "{portfolio.id}" deleted successfully.')
    else:
        response_object = {
            'success': False,
            'message': f'Portfolio with ID "{portfolio.id}" not found.'
        }
        return make_response(jsonify(response_object)), status.HTTP_404_NOT_FOUND


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
    request_body = request.get_json()
    portfolio_name: str = request_body.get('name')

    # TODO: input validation

    try:
        portfolio: models.Portfolio = queries.add_portfolio(portfolio_name, user_id)
    except IntegrityError as e:
        return generate_bad_request_response(f'Portfolio with name "{portfolio_name}" already exists.')
    except Exception as e:
        return generate_internal_error_response('Error creating portfolio.', e)

    return generate_success_response(portfolio.to_json())


@user_portfolios.route('/<portfolio_id>', methods = ['PUT'])
@jwt_required
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
    request_body = request.get_json()
    portfolio_name: str = request_body.get('name')
    
    # TODO: input validation

    # Checking if user already owns a portfolio with this name
    try:
        existing_portfolio = queries.get_portfolio_by_name(user_id, portfolio_name)
    except Exception as e:
        return generate_internal_error_response('Error updating portfolio.', e)
    
    if existing_portfolio is not None:
        return generate_bad_request_response(f'Portfolio with name "{portfolio_name}" already exists. Please choose another name.')


    # Updating Portfolio Name and sending updated portfolio in response
    try:
        portfolio: models.Portfolio = queries.update_portfolio_name(portfolio.id, portfolio_name)
    except Exception as e:
        return generate_internal_error_response('Error updating portfolio.', e)

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
    request_body = request.get_json()
    asset_id: float = request_body.get('asset_id')
    count: float = request_body.get('count')
    buy_price: float = request_body.get('buy_price')
    order_fee: float = request_body.get('order_fee')

    # TODO: input validation

    # Trying to add the element to the portfolio
    try:
        portfolio_element: models.PortfolioElement = queries.add_portfolio_element(portfolio.id, asset_id, count, buy_price, order_fee)
    except Exception as e:
        return generate_internal_error_response('Error adding asset to portfolio.', e)
    
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
    except Exception as e:
        return generate_internal_error_response('Error fetching portfolio element.', e)
    
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
    except Exception as e:
        return generate_internal_error_response('Error deleting portfolio element.', e)
    
    # Check if portfolio was deleted successfully
    if element_deleted == True:
        return generate_success_response(f'Portfolio Element with ID "{p_element_id}" deleted successfully.')
    else:
        response_object = {
            'success': False,
            'message': f'Portfolio Element with ID "{p_element_id}" not found.'
        }
        return make_response(jsonify(response_object)), status.HTTP_404_NOT_FOUND


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
    # TODO: default values to None
    request_body = request.get_json()
    count: float = request_body.get('count')
    buy_price: float = request_body.get('buy_price')
    order_fee: float = request_body.get('order_fee')

    # TODO: input validation
    
    # Trying to update the portfolio element
    try:
        portfolio_element: models.PortfolioElement = queries.update_portfolio_element(portfolio.id, p_element_id, count, buy_price, order_fee)
    except Exception as e:
        return generate_internal_error_response('Error updating portfolio element.', e)
    
    # Check if the portfolio element was deleted because the count was 0 or less
    if portfolio_element == 'deleted':
        return generate_success_response(f'Portfolio Element with ID "{p_element_id}" was deleted because count was zero or less.')
    
    return generate_success_response(portfolio_element.to_json())