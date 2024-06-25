from flask import Request

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
        raise ValueError('Request body needs to be JSON.')

    try:
        request_body = request.get_json()
    except Exception as e:
        raise e
    
    if request_body is None:
        raise ValueError('No JSON data provided.')
    
    return request_body