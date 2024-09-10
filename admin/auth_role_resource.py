from flask import request
from flask_restful import Resource
import admin.auth_role_service as ars
from admin.admin_model import AuthRoleModel

class AuthRoles(Resource):
    def get(self):
        return ars.get_auth_roles()

class AuthRole(Resource):
    def get(self, id):
        return ars.get_auth_role_by_id(id)

class AuthRolePost(Resource):
    def post(self):
        auth_role = AuthRoleModel.parse_obj(request.get_json())
        return ars.upsert_auth_role( auth_role)

class AuthPermissions(Resource):
    def get(self):
        return ars.get_auth_permissions()

class AuthPermission(Resource):
    def get(self, id):
        return ars.get_auth_permission(id)

class AuthPermissionPost(Resource):
    authPermission = {}

    def post(self, id):
        self.authPermission[id] = request.form['authPermission']
        return {'authPermission_id': self.authPermission[id]}

class AuthRolePermissions(Resource):
    def get(self):
        return ars.get_auth_role_permissions()

class AuthRolePermission(Resource):
    def get(self, id):
        return ars.get_auth_role_permission(id)

class AuthRolePermissionPost(Resource):
    authRolePermission = {}

    def post(self, id):
        self.authRolePermission[id] = request.form['authRolePermission']
        return {'authRolePermission_id': self.authRolePermission[id]}