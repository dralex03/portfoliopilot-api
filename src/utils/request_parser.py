from flask import Request

from src.constants.errors import ApiErrors

def parse_json_request_body(request: Request):
    """
    Parses a JSON request body from a flask request.
    Parameters:
        Request request;
    Returns:
        Dict | List: The parsed request body.
    Raises:
        ValueError: If parsing the body fails.
    """
    if not request.is_json:
        raise ValueError(ApiErrors.body_is_not_json)

    try:
        request_body = request.get_json()
    except Exception as e:
        raise e
    
    return request_body