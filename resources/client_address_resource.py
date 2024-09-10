from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.client_address_service as cas

class ClientAddresses(Resource):
    def get(self):
        return cas.get_client_addresses()

class ClientAddress(BaseResource):
    def get(self, id):
        return cas.get_client_address_by_id(id)

    def post( self, id=0):
        return super().post( id, cas.post_client_address)

    def delete(self, id):
        return super().delete( id, cas.delete_client_address_by_id)


class ClientAddressCurrent( Resource):
    def post(self, id=0):
        retval = cas.set_current_address( {"id": id, "is_current": True })
        return retval

class ClientAddressByClient( Resource):
    def get(self, client_id):
        return cas.get_client_addresses_by_client_id(client_id)
