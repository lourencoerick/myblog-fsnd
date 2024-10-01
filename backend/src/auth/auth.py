import json
from urllib.request import urlopen
from functools import wraps
from flask import request, abort

from jose import jwt


AUTH0_DOMAIN = "dev-u87omsusx1w1jtso.us.auth0.com"
ALGORITHMS = ["RS256"]
API_AUDIENCE = "my-blog"

"""
AuthError Exception
A standardized way to communicate auth failure modes
"""


class AuthError(Exception):
    """
    Initialize the AuthError with an error dictionary and status code.

    :param error: A dictionary containing error information (code, description)
    :param status_code: The HTTP status code associated with the error
    """

    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code
        abort(status_code)


# Auth Header


def get_token_auth_header():
    """
    Getting the access token from the header
    """
    auth = request.headers.get("Authorization", None)

    if auth is None:
        raise AuthError(
            {
                "code": "authorization_header_missing",
                "description": "Authorization header is expected.",
            },
            401,
        )

    auth_parts = auth.split(" ")
    bearer, token = auth_parts
    if bearer.lower() != "bearer":
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header" 'must start with "Bearer".',
            },
            401,
        )

    elif len(auth_parts) == 1:
        raise AuthError(
            {"code": "invalid_header", "description": "Token not found."}, 401
        )

    elif len(auth_parts) > 2:
        raise AuthError(
            {
                "code": "invalid_header",
                "description": "Authorization header must be bearer token.",
            },
            401,
        )

    else:
        return token


def check_permissions(permission, payload):
    """
    Checking permission of the recivied token
    """
    if "permissions" not in payload:
        raise AuthError(
            {
                "code": "invalid_claims",
                "description": "Permissions not included in JWT.",
            },
            400,
        )

    # print(payload['permissions'])
    if permission not in payload["permissions"]:
        raise AuthError(
            {"code": "unauthorized", "description": "Permission not found."}, 403
        )
    return True


def verify_decode_jwt(token):
    """
    Checking the recivied jwt
    """
    jsonurl = urlopen(f"https://{AUTH0_DOMAIN}/.well-known/jwks.json")
    jwks = json.loads(jsonurl.read())
    unverified_header = jwt.get_unverified_header(token)
    rsa_key = {}

    if "kid" not in unverified_header:
        raise AuthError(
            {"code": "invalid_header", "description": "Authorization malformed."}, 401
        )

    for key in jwks["keys"]:
        if key["kid"] == unverified_header["kid"]:
            rsa_key = {
                "kty": key["kty"],
                "kid": key["kid"],
                "use": key["use"],
                "n": key["n"],
                "e": key["e"],
            }
    if rsa_key:
        try:
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=ALGORITHMS,
                audience=API_AUDIENCE,
                issuer="https://" + AUTH0_DOMAIN + "/",
            )

            return payload

        except jwt.ExpiredSignatureError as exc:
            raise AuthError(
                {"code": "token_expired", "description": "Token expired."}, 401
            ) from exc

        except jwt.JWTClaimsError as exc:
            raise AuthError(
                {
                    "code": "invalid_claims",
                    "description": "Incorrect claims. "
                    "Please, check the audience and issuer.",
                },
                401,
            ) from exc
        except Exception as exc:
            raise AuthError(
                {
                    "code": "invalid_header",
                    "description": "Unable to parse authentication token.",
                },
                400,
            ) from exc
    raise AuthError(
        {
            "code": "invalid_header",
            "description": "Unable to find the appropriate key.",
        },
        400,
    )


def requires_auth(permission=""):
    """
    Creating a requires_auth decorator factory
    """

    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = get_token_auth_header()
            payload = verify_decode_jwt(token)
            check_permissions(permission, payload)
            return f(*args, **kwargs)

        return wrapper

    return requires_auth_decorator
