from flask import Blueprint, request, make_response, jsonify, current_app
from sqlalchemy.exc import IntegrityError
import json

from src.constants import http_status_codes as status
from src.database import queries, models
from src.utils.decorators import jwt_required

# Create blueprint which is used in the flask app
user_portfolios = Blueprint('portfolio', __name__)


@user_portfolios.route('', methods = ['GET'])
@jwt_required
def get_all_user_portfolios(user_id: str):
    """
    Handles GET requests to /user/portfolios 
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
        response_object = {
            'success': False,
            'message': 'Error fetching all portfolios.',
            'error': str(e)
        }
        return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR

    response_object = {
        'success': True,
        'response': [p.to_json() for p in portfolios]
    }
    return make_response(jsonify(response_object)), status.HTTP_200_OK


@user_portfolios.route('/<portfolio_id>', methods = ['GET'])
@jwt_required
def get_user_portfolio(user_id: str, portfolio_id: str):
    """
    Handles GET requests to /user/portfolios/<portfolio_id> where <portfolio_id> is the ID of a users portfolio.
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    try:
        portfolio: models.Portfolio = queries.get_portfolio_by_id(portfolio_id)
    except Exception as e:
        response_object = {
            'success': False,
            'message': f'Error fetching portfolio with ID "{portfolio_id}"',
            'error': str(e)
        }
        return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if str(portfolio.user_id) == user_id:
        response_object = {
            'success': True,
            'response': portfolio.to_json()
        }
        return make_response(jsonify(response_object)), status.HTTP_200_OK
    else:
        response_object = {
            'success': False,
            'message': f'Portfolio with ID "{portfolio_id}" does not belong to User "{user_id}"'
        }
        return make_response(jsonify(response_object)), status.HTTP_403_FORBIDDEN


@user_portfolios.route('/<portfolio_id>', methods = ['DELETE'])
@jwt_required
def delete_user_portfolio(user_id: str, portfolio_id: str):
    """
    Handles DELETE requests to /user/portfolios/<portfolio_id> where <portfolio_id> is the ID of a users portfolio.
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    try:
        portfolio: models.Portfolio = queries.get_portfolio_by_id(portfolio_id)
    except Exception as e:
        response_object = {
            'success': False,
            'message': f'Error deleting portfolio with ID "{portfolio_id}"',
            'error': str(e)
        }
        return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if portfolio != None and portfolio.user_id != user_id:
        response_object = {
            'success': False,
            'message': f'Portfolio with ID "{portfolio_id}" does not belong to User "{user_id}"'
        }
        return make_response(jsonify(response_object)), status.HTTP_403_FORBIDDEN
    
    try:
        portfolio_deleted = queries.delete_portfolio_by_id(portfolio_id)
    except Exception as e:
        response_object = {
            'success': False,
            'message': f'Error deleting portfolio with ID "{portfolio_id}"',
            'error': str(e)
        }
        return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR
    
    if portfolio_deleted == True:
        response_object = {
            'success': True,
            'response': f'Portfolio with ID "{portfolio_id}" deleted successfully.'
        }
        return make_response(jsonify(response_object)), status.HTTP_200_OK
    else:
        response_object = {
            'success': False,
            'message': f'Portfolio with ID "{portfolio_id}" not found.'
        }
        return make_response(jsonify(response_object)), status.HTTP_404_NOT_FOUND


@user_portfolios.route('/create', methods = ['POST'])
@jwt_required
def create_user_portfolio(user_id: int):
    """
    Handles POST requests to /user/portfolios/create
        Parameters:
            int user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """

    post_data = request.get_json()

    portfolio_name = post_data.get('name')

    try:
        portfolio: models.Portfolio = queries.add_portfolio(portfolio_name, user_id)
        current_app.logger.info(portfolio.to_json())
    except IntegrityError as e:
        response_object = {
            'success': False,
            'message': f'Portfolio with name "{portfolio_name}" already exists.'
        }
        return make_response(jsonify(response_object)), status.HTTP_400_BAD_REQUEST
    except Exception as e:
        response_object = {
            'success': False,
            'message': 'Error creating portfolio.',
            'error': str(e)
        }
        return make_response(jsonify(response_object)), status.HTTP_500_INTERNAL_SERVER_ERROR

    response_object = {
        'success': True,
        'response': portfolio.to_json()
    }
    return make_response(jsonify(response_object)), status.HTTP_200_OK


@user_portfolios.route('/<portfolio_id>/add', methods = ['POST'])
@jwt_required
def add_asset_to_user_portfolio(user_id: str):
    """
    Handles POST requests to /user/portfolios/<portfolio_id>/add where <portfolio_id> is the ID of a users portfolio.
        Parameters:
            str user_id;
        Returns:
            tuple:
                Response: Flask Response, contains the response_object dict
                int: the response status code
    """
    # TODO