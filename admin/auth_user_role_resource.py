from flask import request
from flask_restful import Resource
import admin.auth_user_service as aus

authUserRole = {}


class AuthUserRoles(Resource):
    def get(self):
        return aus.get_auth_user_role()


class AuthUserRole(Resource):
    def get(self, id: int):
        return aus.get_auth_user_role(id)

    def put(self, id: int):
        authUserRole[id] = request.form["authUserRole"]
        return {"authUserRole_id": authUserRole[id]}
