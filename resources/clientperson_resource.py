from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.client_person_service as cps

clientPerson = {}
class ClientPersons(Resource):
    def get(self):
        return cps.get_client_persons()

class ClientPerson(BaseResource):
    def get(self, id):
        return cps.get_client_person_by_id(id)

    def post(self, id=0):
        return super().post( id, cps.post_client_person)

    def delete(self, id=0):
        return cps.delete_client_person_by_id(id)
