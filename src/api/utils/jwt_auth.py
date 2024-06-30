import datetime

import jwt

from src.config import JWT_EXPIRY, JWT_SECRET_KEY
from src.constants.errors import ApiErrors


def encode_auth_token(user_id: str):
    """
    Generates the JWT Auth Token.
        Parameters:
            str user_id;
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
        return None


def decode_auth_token(auth_token: str):
    """
    Decodes and validates the JWT auth token
        Parameters:
            str auth_token;
        Returns:
            tuple:
                bool: True if the auth token is valid, else False
                str: the user_id, if the token is valid
    """

    try:
        payload = jwt.decode(
            auth_token,
            JWT_SECRET_KEY,
            algorithms=['HS256'],
            options={
                'verify_signature': True
            }
        )
        return (True, payload['sub'])
    except jwt.ExpiredSignatureError:
        return (False, ApiErrors.JwtAuth.jwt_token_expired)
    except jwt.InvalidTokenError:
        return (False, ApiErrors.JwtAuth.jwt_token_invalid)