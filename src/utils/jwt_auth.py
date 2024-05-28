import jwt
import datetime

from src.config import JWT_EXPIRY, JWT_SECRET_KEY

def encode_auth_token(user_id):
    """
    Generates the JWT Auth Token.
        Parameters:
            user_id: str
        Returns:
            str: The JWT Token
    """

    try:
        payload = {
            'exp': datetime.datetime.now(datetime.UTC) + JWT_EXPIRY,
            'iat': datetime.datetime.now(datetime.UTC),
            'sub': user_id
        }
        return jwt.encode(
            payload,
            JWT_SECRET_KEY,
            algorithm='HS256'
        )
    except Exception as e:
        print("Error generating JWT Token: " + e)
        return None
    
def decode_auth_token(auth_token):
    """
    Decodes and validates the JWT auth token
        Parameters:
            auth_token: str
        Returns:
            bool: True if the auth token is valid
            int: the user_id, if the token is valid
    """

    try:
        payload = jwt.decode(auth_token, JWT_SECRET_KEY)
        return True, payload['sub']
    except jwt.ExpiredSignatureError:
        return False, 'Signature expired. Please log in again.'
    except jwt.InvalidTokenError:
        return False, 'Invalid token. Please log in again.'