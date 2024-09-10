import os
from flask import request
from flask_restful import Resource
import datetime
import jwt
import admin.user_login_service as uls


jwt_key = 'junior'

# import parse_token, login, register
class Login(Resource):
    def get(self):
        authToken = uls.parse_token( request)
        if authToken is not None:
            try:
                jwt_key = os.getenv('JWT_SECRET_KEY')
                payload = jwt.decode(authToken, jwt_key, algorithms=["HS256"])
                exp = datetime.datetime.fromtimestamp( payload['exp'])
                expTime = exp.strftime( "%Y-%m-%d %H:%M:%S")
                return { 'rc': -1, 'msg': payload, 'exp': expTime}
            except jwt.ExpiredSignatureError:
                return { 'rc': -1, 'msg': 'Token expired'}
            except jwt.InvalidSignatureError:
                return { 'rc': -1, 'msg': 'Invalid Signature Error'}
        return { 'rc': -9, 'msg': 'No Authorization Token'}

    def post(self, name):
        funcs = {
            'login': uls.login,
            'logout': uls.logout,
            'register': uls.register,
            'user': uls.get_user
        }
        if name in funcs:
            return {name: funcs[name]() }, 200
        return None, 404

