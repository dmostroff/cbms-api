from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.credit_line_history_service as clhs

class CreditLineHistories(Resource):
    def get(self):
        return clhs.get_credit_line_histories()

class CreditLineHistory(BaseResource):
    def get(self, id):
        return clhs.get_credit_line_history_by_id(id)

    def post(self, id=0):
        return super().post( id, clhs.post_credit_line_history)

    def delete( self, id):
        return clhs.delete_credit_line_history_by_id(id)

class CreditLineHistoryByClient(Resource):
    def get(self, client_id):
        return clhs.get_credit_line_history_by_client_id(client_id)
