from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.client_israel_service as cis


class ClientIsraels(Resource):
    def get(self):
        return cis.get_client_israels()

class ClientIsraelsByClient(Resource):
    def get(self, client_id):
        return cis.get_client_israel_by_client(client_id)

class ClientIsrael(BaseResource):
    def get(self, id):
        return cis.get_client_israel_by_id(id)

    def post(self, id=None):
        return super().post( id, cis.post_client_israel)

    def delete(self, id):
        return cis.delete_client_israel_by_id( id)
