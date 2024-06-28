from flask import Blueprint, request, make_response, jsonify

from src.database import queries
from src.database.models import User
from src.constants import http_status_codes as status
from src.utils.responses import *
from src.utils.request_parser import *
from src.constants.errors import ApiErrors
from src.constants.messages import ApiMessages
from src.constants.countries import COUNTRIES
from src.market_data.search import search_assets


# Create blueprint which is used in the flask app
assets = Blueprint('assets', __name__)


@assets.route('/search', methods=['GET'])
def refresh_session():
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
        return generate_bad_request_response(ApiErrors.Assets.search_missing_query)
    
    # "country" is optional, but needs to be valid
    # if its not valid, we default it to None
    if isinstance(country, str) and len(country) > 0:
        if country not in COUNTRIES:
            country = None
    else:
        country = None

    return generate_success_response(search_assets(query, country))
    
    