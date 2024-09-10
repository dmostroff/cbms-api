from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.checking_service as cs


class Checkings(Resource):
    def get(self):
        return cs.get_checkings()

class Checking(BaseResource):
    def get(self, id):
        return cs.get_checking_by_id(id)

    def post(self, id=0):
        return super().post( id, cs.post_checking)

    def delete( self, id):
        return cs.delete_checking_by_id(id)

class CheckingByClient(Resource):
    def get(self, client_id):
        return cs.get_checking_by_client_id(client_id)
