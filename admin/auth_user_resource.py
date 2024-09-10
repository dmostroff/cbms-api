from flask_restful import Resource
import admin.auth_user_service as aus

authUser = {}
class AuthUsers(Resource):
    def get(self):
        return aus.get_auth_users()

class AuthUser(Resource):
    def get(self, id):
        return aus.get_auth_user(id)

    def put(self, id):
        authUser[id] = request.form['authUser']
        return {'authUser_id': authUser[id]}

    def post(self):
        authUserJson = request.get_json()
        return {'authUser_id': authUserModel}
