from flask.testing import FlaskClient

from src.constants.errors import ApiErrors


def login_user(client: FlaskClient, email: str, password: str) -> str:
    """
    Helper function that uses the test client to login a user
    and return the valid auth token.
        Parameters:
            FlaskClient client;
            str email;
            str password;
        Returns:
            str: the auth token.
    """
    response = client.post('/user/login',
                           json={
                               'email': email,
                               'password': password
                           })

    response_json = response.get_json()
    if 'message' in response_json and response_json['message'] == ApiErrors.User.login_invalid_credentials:
        return register_user(client, email, password)

    assert response.status_code == 200

    return response.json['response']['auth_token']


def register_user(client: FlaskClient, email: str, password: str) -> str:
    """
    Helper function that uses the test client to register a new user
    and return the valid auth token.
        Parameters:
            FlaskClient client;
            str email;
            str password;
        Returns:
            str: the auth token.
    """
    response = client.post('/user/register',
                           json={
                               'email': email,
                               'password': password
                           })

    assert response.status_code == 200

    return response.json['response']['auth_token']


def create_portfolio(client: FlaskClient, auth_token: str, name: str) -> str:
    """
    Helper function that uses the test client to create a new portfolio
    for a given user (auth_token).
        Parameters:
            FlaskClient client;
            str auth_token;
            str name;
        Returns:
            str: the ID of the new portfolio.
    """
    response = client.post('/user/portfolios/create',
                           json={
                               'name': name
                           },
                           headers={
                               'Authorization': 'Bearer ' + auth_token
                           })

    assert response.status_code == 200

    return response.json['response']['id']


def get_portfolio(client: FlaskClient, auth_token: str, name: str) -> str:
    """
    Helper function that uses the test client to get an existing portfolio
    for a given user (auth_token).
    If portfolio doesnt exist, its created.
        Parameters:
            FlaskClient client;
            str auth_token;
            str name;
        Returns:
            str: the ID of the portfolio.
    """
    response = client.get('/user/portfolios',
                          headers={
                              'Authorization': 'Bearer ' + auth_token
                          })

    assert response.status_code == 200

    try:
        portfolio_id = next(
            p for p in response.json['response'] if p['name'] == name
        )['id']
    except:
        portfolio_id = None

    if portfolio_id is None:
        return create_portfolio(client, auth_token, name)

    return portfolio_id
