from flask_restful import Resource
from resources.base_resource import BaseResource
import clients.client_loan_service as cs


class ClientLoans(Resource):
    def get(self):
        return cs.get_client_loans()

class ClientLoan(BaseResource):
    def get(self, id):
        return super().get(id, cs.get_client_loan_by_id)

    def post(self, id=0):
        return super().post(id, cs.post_client_loan)

    def delete( self, id):
        return cs.delete_client_loan_by_id(id)

class ClientLoanByClient(Resource):
    def get(self, client_id):
        return cs.get_client_loan_by_client_id(client_id)
