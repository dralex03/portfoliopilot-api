from flask.testing import FlaskClient

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
    
    return response.json['response']['auth_token']