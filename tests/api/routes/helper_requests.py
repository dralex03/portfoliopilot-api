from flask.testing import FlaskClient

def login_user(client: FlaskClient, email: str, password: str) -> str:
    response = client.post('/user/login',
                                json={
                                    'email': email,
                                    'password': password
                                })
    
    return response.json['response']['auth_token']