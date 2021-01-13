import json
from flask import (
    request,
    session,
    url_for,
    redirect,
    Blueprint)
from jose import jwt
from urllib.request import urlopen
from functools import wraps

# Local imports...
from config import Config
from exceptions import AuthError

auth_bp = Blueprint('auth_bp', __name__)

###########################################################
#
# CONSTANTS
#
###########################################################

conf = Config()

api_audience = conf.API_AUDIENCE
auth0_domain = conf.AUTH0_DOMAIN
algorithms = conf.ALGORITHMS
client_id = conf.CLIENT_ID
client_secret = conf.CLIENT_SECRET
access_token_url = conf.ACCESS_TOKEN_URL
authorize_url = conf.AUTHORIZE_URL
callback_uri = conf.CALLBACK_URL
secret_key = conf.SECRET_KEY
test_token = conf.TEST_TOKEN
conf_access_key = conf.ACCESS_KEY
profile_key = conf.PROFILE_KEY


'''
    Implement _get_token_auth_header() method
    it should attempt to get the header from the request
        it should raise an AuthError if no header is present
    it should attempt to split bearer and the token
        it should raise an AuthError if the header is malformed
    return the token part of the header
'''


def _get_token_auth_header():

    #############################################################
    #
    # TODO This is not the correct way to implement security,
    # I'd imagine that one should be passing the access key
    # between the front end and back end through the request
    # header. However, I have spend two weeks trying different
    # ways and still couldn't come up with a feasible solution.
    # Since this part is not critical for the capstone, I have
    # implemented this temporary solution to force the
    # application to work, and I will try to figure it out in
    # a later time.
    #
    # This implementation does not grab the access token from
    # the request header, but check the host url from the request
    # header and see if it's the same as the 'API Audience' set
    # up using the Auth0 API UI. If it is, grab the access key
    # stored in the Flask session when the application is going
    # through the callback code after logging in. And all the
    # steps after that follow strictly to how we are taught.
    #
    ###############################################################

    if request.headers['HOST'] in api_audience:
        # Postman test work-around
        if 'POSTMAN_TOKEN' not in request.headers:
            # Unit test work-around
            if 'test_permission' in request.headers:
                return test_token

            if conf_access_key in session:
                access_key = session[conf_access_key]
                return access_key['access']
            else:
                raise AuthError({
                    "code": "authorization_required",
                    "description": "User is not logged in"
                }, 401)

    if 'Authorization' not in request.headers:
        raise AuthError({
            "code": "authorization_required",
            "description": "Authorization is expected in header"
        }, 401)

    # "Authorization": "bearer <<token>>"
    auth_header = request.headers['Authorization']

    header_parts = auth_header.split(' ')

    if len(header_parts) != 2 or header_parts[0].lower() != 'bearer':
        raise AuthError({
            "code": "invalid_token",
            "description": "Mendatory authorization requires 'bearer' token"
        }, 401)

    return header_parts[1]


'''
    Implement check_permissions(permission, payload) method
    @INPUTS
        permission: string permission (i.e. 'post:drink')
        payload: decoded jwt payload

    it should raise an AuthError if permissions are not included in the payload
        !!NOTE check your RBAC settings in Auth0
    it should raise an AuthError if the requested permission string is
    not in the payload permissions array
    return true otherwise
'''


def _check_permissions(permission, payload):
    if 'permissions' not in payload:
        raise AuthError({
            'code': 'invalid_claims',
            'description': 'Permissions not included in JWT'
        }, 400)

    # For unit testing purposes
    # The key-value pair of 'test_permission' is included in the request
    # headers when the request is identified as an unit test request;
    # permissions of the routes then can be tested via the manipulations of
    # the permissions list in the payload
    if 'test_permission' in request.headers:
        payload['permissions'] = [request.headers['test_permission']]

    if isinstance(permission, list) and len(permission) > 1:
        if not set(permission).intersection(payload['permissions']):
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found'
            }, 401)
    else:
        if permission not in payload['permissions']:
            raise AuthError({
                'code': 'unauthorized',
                'description': 'Permission not found'
            }, 401)

    return True


'''
    Implement verify_decode_jwt(token) method
    @INPUTS
        token: a json web token (string)

    it should be an Auth0 token with key id (kid)
    it should verify the token using Auth0 /.well-known/jwks.json
    it should decode the payload from the token
    it should validate the claims
    return the decoded payload

    !!NOTE urlopen has a common certificate error described here:
    https://stackoverflow.com/questions/50236117/scraping-ssl-certificate-verify-failed-error-for-http-en-wikipedia-org
'''


def _verify_decode_jwt(token):
    # Get the public key from Auth0
    jsonurl = urlopen(
        f'https://{auth0_domain}/.well-known/jwks.json')
    jwks = json.loads(jsonurl.read())

    # Get the data in the header
    unverified_header = jwt.get_unverified_header(token)

    # Choose the key
    rsa_key = {}
    if 'kid' not in unverified_header:
        raise AuthError({
            'code': 'invalid_header',
            'description': 'Authorization malformed'
        }, 401)

    for key in jwks['keys']:
        if key['kid'] == unverified_header['kid']:
            rsa_key = {
                'kty': key['kty'],
                'kid': key['kid'],
                'use': key['use'],
                'n': key['n'],
                'e': key['e']
            }

    # Finally, verify!!!
    if rsa_key:
        try:
            # USE THE KEY TO VALIDATE THE JWT
            payload = jwt.decode(
                token,
                rsa_key,
                algorithms=algorithms,
                audience=api_audience,
                issuer=(
                    f'https://{auth0_domain}/')
            )

            return payload

        except jwt.ExpiredSignatureError:
            raise AuthError({
                'code': 'token_expired',
                'description': 'Token expired'
            }, 401)

        except jwt.JWTClaimsError:
            raise AuthError({
                'code': 'invalid_claims',
                'description':
                    'Incorrect claims. Please check the audience and issuer'
            }, 401)
        except Exception:
            raise AuthError({
                'code': 'invalid_header',
                'description': 'Unable to parse authentication token'
            }, 400)
    raise AuthError({
        'code': 'invalid_header',
        'description': 'Unable to find the appropriate key'
    }, 400)


def requires_auth(permission=''):
    def requires_auth_decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = _get_token_auth_header()
            try:
                payload = _verify_decode_jwt(token)
            except BaseException:
                raise AuthError({
                    "code": "jwt_decode_error",
                    "description": "Error decoding JWT"
                }, 401)

            _check_permissions(permission, payload)

            return f(payload, *args, **kwargs)

        return wrapper
    return requires_auth_decorator


def requires_login(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if profile_key not in session:
            session.clear()
            return redirect(url_for('login'))
        return f(*args, **kwargs)

    return decorated
