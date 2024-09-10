# user_login_service
from flask import current_app
from flask import request
import datetime
import os
import jwt
import admin.auth_user_service as aus
import admin.user_login_repository as ulr
import common.base_service as bs
from common.common_service import json_rc_msg
from models.UserLoginModel import UserLoginModel
from models.AuthUserModel import AuthUserModel
from models.UserLoginModel import UserLoginModel
from models.AuthUserModel import AuthUserModel

JWT_CRYPT_ALG="HS256"
# AUTHORIZATION="Authorization"
AUTHORIZATION="auctoritas"

def dump_headers( request):
    current_app.logger.info( "--- Headers ---")
    for k in request.headers.keys():
        header_val = request.headers.get(k)
        current_app.logger.info( f"{k}={header_val}")
    current_app.logger.info( "--- end Headers ---")


def parse_token( request):
    # dump_headers( request)
    authToken = request.headers.get( AUTHORIZATION)
    current_app.logger.info( f"authToken: {authToken}")
    return authToken

def get_token( request):
    # dump_headers( request)
    return request.headers.get( AUTHORIZATION)

def create_token( username):
    jwt_token = None
    seconds_expiry = int(os.getenv( 'LOGIN_TIMEOUT',str(5*60*60)))
    payload = {'username': username, "exp": datetime.datetime.utcnow() + datetime.timedelta(seconds=seconds_expiry)}
    jwt_key = os.getenv('JWT_SECRET_KEY')
    try:
        jwt_token = jwt.encode(payload, jwt_key, algorithm=JWT_CRYPT_ALG)
    except jwt.exceptions.InvalidKeyError:
        current_app.logger.error( json_rc_msg(-1, "invalid key"))
        raise jwt.exceptions.InvalidKeyError
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return jwt_token

def decrypt_token( auth_token ):
    retval = { 'rc': 0, 'msg': 'No token', 'data': None}
    if auth_token is None:
        return retval
    jwt_token_decode = None
    jwt_key = os.getenv('JWT_SECRET_KEY')
    try:
        jwt_token_decode = jwt.decode(auth_token, jwt_key, algorithms=JWT_CRYPT_ALG)
        retval = json_rc_msg( 1, 'Valid', jwt_token_decode )
        # current_app.logger.info( jwt_token_decode)
        dt = datetime.datetime.fromtimestamp(jwt_token_decode.get('exp'))
        # current_app.logger.info( f"Exp date: {dt.strftime('%Y-%m-%d %H:%M:%S')}.")
    except jwt.exceptions.InvalidKeyError:
        retval = json_rc_msg( -8, 'Invalid key')
        current_app.logger.error( retval)
    except jwt.exceptions.ExpiredSignatureError:
        retval = json_rc_msg( -8, 'Expired')
        current_app.logger.error( retval)
    except Exception as ex:
        current_app.logger.error( repr(ex))
        raise ex
    finally:
        return retval

def add_token_to_header( response, username):
    if response is not None:
        auth_token = create_token( username)
        # current_app.logger.info(f"add_token_to_header {username} {AUTHORIZATION} {auth_token}")
        response.headers.set( AUTHORIZATION, auth_token)
    return response

def is_valid_token( token_result):
    if token_result is None:
        return False
    return True if 'rc' in token_result and token_result['rc'] == 1 else False

def get_username_from_token_result( token_result):
    return token_result['data']['username'] if is_valid_token(token_result) else None

def token_result_from_request( request):
    return decrypt_token( get_token( request))

def update_token( request, response):
    token_result = decrypt_token( get_token( request))
    if is_valid_token( token_result):
        response = add_token_to_header( response, token_result['data']['username'])
    return response

#--------------------
# user_login
#--------------------
def login(user_dict):
    try:
        user_login = login_authenticate( user_dict['username'], user_dict['pwd'])
        if user_login['user'] is None:
            return json_rc_msg( 0, 'Invalid Login', user_login)
        if user_login['user_login'] is None:
            return json_rc_msg( 0, 'Invalid Login', user_login)
        return json_rc_msg(1, 'Login successful', user_login )
    except jwt.exceptions.InvalidKeyError:
        current_app.logger.error( "InvalidKey")
        return json_rc_msg( -1, 'Invalid key')
    except Exception as ex:
        retval = json_rc_msg(-9, "Error", repr(ex))
        current_app.logger.error( retval)
        return retval

def login_authenticate( username, password):
    user = aus.authenticate_user( username, password)
    newUserLogin = None
    if user is not None:
        jwt_token = create_token( user['username'])
        userLogin = UserLoginModel.parse_obj( { 'username': user['username'], 'startpage': 'clients', 'token': jwt_token })
        newUserLogin = upsert_user_login( userLogin)
        user.pop('password', None)
    else:
        user = { 'username': username, 'isValid': False } # aus.get_auth_user_by_username(username)
    user_login = newUserLogin['data'] if newUserLogin is not None and 'data' in newUserLogin else None
    return { 'user': user, 'user_login': user_login}

def logout():
    jwt_token_decode = decrypt_token(get_token(request))
    if jwt_token_decode.get('username') is not None:
        ulr.delete_user_login_by_username(jwt_token_decode['username'])
    return json_rc_msg( 1, 'Logged out')

def register(auth_user_dict):
    auth_user = AuthUserModel.parse_obj( auth_user_dict)
    try:
        user_login = onboard_register( auth_user)
        return json_rc_msg( 0, 'Login', user_login )
    except jwt.exceptions.InvalidKeyError:
        return json_rc_msg( -1, 'Invalid key')
    except Exception as ex:
        current_app.logger.error( f"register] {repr(ex)}")
        return json_rc_msg( -9, repr(ex))

def onboard_register( auth_user:AuthUserModel):
    user = aus.upsert_auth_user( auth_user)
    if user['rc'] == 1:
        return login_authenticate( user['data']['username'], user['data']['password'])
    return user

@bs.repository_call_single_row
def get_user_login():
    pass

@bs.repository_call
def get_user_logins():
    return ulr.get_user_logins()

@bs.repository_call_single_row
def upsert_user_login( userLogin: UserLoginModel):
    return ulr.upsert_user_login( userLogin)

def authenticate_user( username, password):
    pass

@bs.repository_call
def get_auth_user( username, jwt_token, user_login:UserLoginModel):
    return ulr.upsert_user_login( user_login)
